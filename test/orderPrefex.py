__author__ = 'seven.wang'

def num(str1):
    result = 0
    for c in str1:
        result *= 36
        ordc = ord(c)
        if 97 <= ordc < (97+26):
            result += ord(c)-97+10
        else:
            result += int(c)
    return result


file1 = "E:\\PycharmProjects\\My\\test\\order_prefix.txt.out.out.3"
fo = open(file1, 'r')
for line in fo:
    arr =line.split(" ")
    # print arr[0], arr[1],
    print arr[0], num(arr[0]), arr[1],


