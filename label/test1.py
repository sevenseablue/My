# coding: utf8


__author__ = 'seven.wang'

import os, sys

import cv2
from traits.api import HasTraits, Str, Int


class SimpleEmployee(HasTraits):
    index = Str
    name = Str


dir1 = "E:\PycharmProjects\My\label\data"
pics = os.listdir(dir1)
# print "exit"
picInd = 0
for picInd in range(len(pics)):
    img = cv2.imread("%s/%s" % (dir1, pics[picInd]))
    cv2.namedWindow("Image")
    cv2.imshow("Image", img)


    sam = SimpleEmployee()
    sam.configure_traits()
    print pics[picInd], sam.index, sam.name
    cv2.waitKey(1)

cv2.destroyAllWindows()

sys.exit(0)


