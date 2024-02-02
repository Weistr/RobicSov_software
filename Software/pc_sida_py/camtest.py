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

video_photo0 = cv2.VideoCapture(1) #上

while 
S = input('开始')
ret0, frame0 = video_photo0.read()
cv2.imwrite(str(0) + '.jpg', frame0)
img0 = cv2.imread('000.jpg')  # 图片0,识别左F,右R
hsv0 = cv2.cvtColor(img0, cv2.COLOR_BGR2HSV)
print("拍照成功")