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




print("正在开启相机......")
video_photo0 = cv2.VideoCapture(1) #上
video_photo1 = cv2.VideoCapture(4) #下
video_photo2 = cv2.VideoCapture(3) #
video_photo3 = cv2.VideoCapture(2) #
video_photo0.set(cv2.CAP_PROP_AUTO_EXPOSURE,0)
video_photo0.set(cv2.CAP_PROP_AUTO_WB,0)
video_photo0.set(cv2.CAP_PROP_EXPOSURE,-10)
video_photo1.set(cv2.CAP_PROP_AUTO_EXPOSURE,0)
video_photo1.set(cv2.CAP_PROP_AUTO_WB,0)
video_photo1.set(cv2.CAP_PROP_EXPOSURE,-10)
video_photo2.set(cv2.CAP_PROP_AUTO_EXPOSURE,0)
video_photo2.set(cv2.CAP_PROP_AUTO_WB,0)
video_photo2.set(cv2.CAP_PROP_EXPOSURE,-10)
video_photo3.set(cv2.CAP_PROP_AUTO_EXPOSURE,0)
video_photo3.set(cv2.CAP_PROP_AUTO_WB,0)
video_photo3.set(cv2.CAP_PROP_EXPOSURE,-10)
# 拍照上###################################################################################
S = input('相机已开启，准备识别')
ret0, frame0 = video_photo0.read()
cv2.imwrite(str(0) + '.jpg', frame0)
img0 = cv2.imread('0.jpg')  # 图片0,识别左F,右R
hsv0 = cv2.cvtColor(img0, cv2.COLOR_BGR2HSV)
print("上面拍照成功")
video_photo0.release()
# 拍照1###################################################################################

# 拍照下###################################################################################
ret1, frame1 = video_photo1.read()
cv2.imwrite(str(1) + '.jpg', frame1)
img1 = cv2.imread('1.jpg')  # 图片2,识别左L,右B
hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
print("下面拍照成功")
video_photo1.release()
# 拍照2###################################################################################

# 拍照左###################################################################################
ret2, frame2 = video_photo2.read()
cv2.imwrite(str(2) + '.jpg', frame2)
img2 = cv2.imread('2.jpg')  # 图片3,识别D
hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
print("左拍照成功")
video_photo2.release()
# 拍照3###################################################################################

# 拍照右###################################################################################
ret3, frame3 = video_photo3.read()
cv2.imwrite(str(3) + '.jpg', frame3)
img3 = cv2.imread('3.jpg')  # 图片1,识别U
hsv3 = cv2.cvtColor(img3, cv2.COLOR_BGR2HSV)
print("右拍照成功")
video_photo3.release()
