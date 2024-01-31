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



Video = cv2.VideoCapture(0) #设置摄像头 0是默认的摄像头 如果你有多个摄像头的话呢，可以设置1,2,3....
ret,frame = Video.read() #将摄像头拍到的图像作为frame值
cv2.imshow('video',frame) #将frame的值显示出来 有两个参数 前一个是窗口名字，后面是值
print('宽:', Video.get(cv2.CAP_PROP_FRAME_WIDTH) )
print('高:', Video.get(cv2.CAP_PROP_FRAME_HEIGHT) )
print('帧率:', Video.get(cv2.CAP_PROP_FPS) )
print('亮度:', Video.get(cv2.CAP_PROP_BRIGHTNESS) )
print('对比度:', Video.get(cv2.CAP_PROP_CONTRAST) )
print('饱和度:', Video.get(cv2.CAP_PROP_SATURATION) )
print('色调:', Video.get(cv2.CAP_PROP_HUE) )
print('曝光度:', Video.get(cv2.CAP_PROP_EXPOSURE) )
print('asdasdsadas')


Video.set(cv2.CAP_PROP_EXPOSURE, -10)  # 曝光 -1
ret,frame = Video.read() #将摄像头拍到的图像作为frame值
cv2.imshow('video2',frame) #将frame的值显示出来 有两个参数 前一个是窗口名字，后面是值
print('宽:', Video.get(cv2.CAP_PROP_FRAME_WIDTH) )
print('高:', Video.get(cv2.CAP_PROP_FRAME_HEIGHT) )
print('帧率:', Video.get(cv2.CAP_PROP_FPS) )
print('亮度:', Video.get(cv2.CAP_PROP_BRIGHTNESS) )
print('对比度:', Video.get(cv2.CAP_PROP_CONTRAST) )
print('饱和度:', Video.get(cv2.CAP_PROP_SATURATION) )
print('色调:', Video.get(cv2.CAP_PROP_HUE) )
print('曝光度:', Video.get(cv2.CAP_PROP_EXPOSURE) )
print('asdasdsadas')


while True:   #进入无限循环
    c = cv2.waitKey(1) #判断退出的条件 当按下'Q'键的时候呢，就退出
    if c == ord('q'):
        break
#Video.release()  #常规操作