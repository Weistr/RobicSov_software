import cv2
import kociemba
import time
import serial
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

import skimage
from skimage import draw
from skimage import morphology
from skimage import data

from copy import deepcopy
from copy import deepcopy
import heapq

PixelHsvAarry = []
num = 3
def cube_color(PixelPosXy, hsv_img, z):
    for k in range(len(PixelPosXy)):
        for i in range(num):
            for j in range(num):
                PixelHsvAarry.append(
                    [int(hsv_img[[PixelPosXy[k][1]+j-int(num/2)], [PixelPosXy[k][0]+i-int(num/2)]][0][0]),
                     int(hsv_img[[PixelPosXy[k][1]+j -int(num/2)], [PixelPosXy[k][0]+i-int(num/2)]][0][1]),
                     int(hsv_img[[PixelPosXy[k][1]+j-int(num/2)], [PixelPosXy[k][0]+i-int(num/2)]][0][2])
                     ]
                    )
                    
                    
# 坐标上
PixelPosXy_0 = [[206, 117], [255, 113], [329, 104],
                [198, 216], [257, 223], [322, 225],
                [203, 316], [254, 327], [325, 345],
                [412, 100], [485, 114], [549, 120],
                [414, 227], [488, 224], [549, 219],
                [412, 350], [490, 331], [549, 316]]
# 坐标下
PixelPosXy_1 = [[250, 170], [265, 100], [270, 50],
                [350, 175], [350, 110], [355, 55],
                [455, 175], [445, 110], [440, 55],
                [255, 360], [255, 310], [250, 245],
                [345, 365], [350, 315], [350, 250],
                [430, 365], [445, 315], [455, 250]]

# 坐标左
PixelPosXy_2 = [[135, 215], [225, 120], [315, 60],
                [227, 313], [334, 220], [426, 127],
                [328, 397], [443, 312], [500, 205],
                ]
# 坐标右
PixelPosXy_3 = [[327, 425], [227, 343], [131, 242], 
                [423, 338], [324, 224],  [227, 133], 
                [507, 230], [407, 135], [315, 60],
                ]
            

s = input("choose pix(U1,F2....)")
U_imgId = [3,7,11,15,19,27]#g o b r y w
img = [[],[],[],[],[],[]]
hsv = [[],[],[],[],[],[]]
pixArr = []
if s[0] == 'U':
    for pix in range(6) :
        img[pix] = cv2.imread(str(U_imgId[pix])+'.jpg')  # 图片1,识别U
        hsv[pix] = cv2.cvtColor(img[pix], cv2.COLOR_BGR2HSV)
        k = int(s[1])
        print("****pixarr******")
        hsum =0 
        ssum = 0
        vsum = 0
        for i in range(num):
            for j in range(num):
                hsum += int(hsv[pix][[PixelPosXy_3[k][1]+j-int(num/2)], [PixelPosXy_3[k][0]+i-int(num/2)]][0][0])
                ssum += int(hsv[pix][[PixelPosXy_3[k][1]+j-int(num/2)], [PixelPosXy_3[k][0]+i-int(num/2)]][0][1])
                vsum += int(hsv[pix][[PixelPosXy_3[k][1]+j-int(num/2)], [PixelPosXy_3[k][0]+i-int(num/2)]][0][2])
        hsum = hsum // 9
        ssum = ssum // 9
        vsum = vsum // 9
        pixArr=[hsum,ssum,vsum]
        print(pixArr)
        cv2.imshow(str(pix),img[pix])

    
cv2.waitKey(0)