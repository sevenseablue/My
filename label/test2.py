# coding: utf8


__author__ = 'seven.wang'

import os, sys

import cv2
from traits.api import HasTraits, Str, Int
import numpy as np


dir1 = "E:\PycharmProjects\My\label\data"
pics = os.listdir(dir1)
# print "exit"
picInd = 2
outDir = "E:\PycharmProjects\My\label\dataSplit"

for picInd in range(len(pics)):
    img = cv2.imread("%s/%s" % (dir1, pics[picInd]))
    # print img.shape
    # cv2.namedWindow("Image")
    # cv2.imshow("Image", img[1:30, 118:])
    # cv2.imwrite("Image_head.png", img[1:30, 118:])
    # cv2.waitKey(0)
    width = 73
    height = 80
    h1 = [30, 30 + height]
    h2 = [30 + height, 30 + 2 * height]
    img_list = [img[1:30, 118:],
                img[h1[0]:h1[1], 0:width], img[h1[0]:h1[1], width:width*2],
                img[h1[0]:h1[1], width*2:width*3], img[h1[0]:h1[1], width*3:width*4],
                img[h2[0]:h2[1], 0:width], img[h2[0]:h2[1], width:width*2],
                img[h2[0]:h2[1], width*2:width*3], img[h2[0]:h2[1], width*3:width*4]]

    for i in range(len(img_list)):
        print i
        cv2.imwrite("%s/%s_%s.png" % (outDir, pics[picInd], img_list[i]))


# cv2.destroyAllWindows()

sys.exit(0)


