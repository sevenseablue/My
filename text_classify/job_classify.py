# coding: utf8


__author__ = 'seven.wang'


import pickle
import numpy
numpy.random.seed(42)


def get_cols(f1, delim="\001", cols=0):
    f_o = open(f1, 'r')
    result = []
    for line in f_o:
        l1 = line.rstrip("\n").split(delim)
        result.append(l1[cols].decode("utf-8"))
    return result


f1 = "data/data.txt"
word_data = get_cols(f1, cols=0)
target_data = get_cols(f1, cols=1)

### test_size is the percentage of events assigned to the test set (remainder go into training)
from sklearn import cross_validation
features_train1, features_test1, labels_train, labels_test = cross_validation.train_test_split(word_data, target_data, test_size=0.1, random_state=42)

print features_test1[0], labels_test[0]

f_stop_words = "data/stop_words.txt"
stop_words = get_cols(f_stop_words, cols=0)

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                             stop_words=stop_words)
features_train = vectorizer.fit_transform(features_train1).toarray()
features_test  = vectorizer.transform(features_test1).toarray()

print features_train.shape
print features_test.shape
print len(labels_train)
print len(labels_test)
print


### a classic way to overfit is to use a small number
### of data points and a large number of features
### train on only 150 events to put ourselves in this regime
features_train = features_train[:]
labels_train = labels_train[:]



### your code goes here
# from sklearn import tree
# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(features_train, labels_train)


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=37)
clf.fit(features_train, labels_train)

pred = clf.predict(features_test)
print(len(labels_test))
print(len(pred))
print(sum(pred == labels_test))

for i in range(len(pred)):
    if pred[i] != labels_test[i]:
        print features_test1[i], labels_test[i], pred[i]


fia = clf.feature_importances_
max = 0.0
maxInd = -1

fia_enum = sorted(list(enumerate(fia)), key=lambda (x, y): -y)
print fia_enum[:10]
index_1 = zip(*fia_enum[:10])[0]
for i in index_1:
    print vectorizer.get_feature_names()[i]


