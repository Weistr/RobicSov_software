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
def calculate_crc16(pmotionResult):  # CRC校验
    # sarray=发送数组
    data = pmotionResult[0]
    crc = 0xFFFF
    for char in data:
        crc ^= ord(char)
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    # 计算校验值并输出结果
    crc = hex(crc)[2:].zfill(4).upper()
    pmotionResult[1] += crc[2]+crc[3]
    pmotionResult[2] += crc[0]+crc[1]

    #print("CRC16校验值为:", crc)
    #print(motionResult)

    array = []
    for j in range(len(pmotionResult)):
        if j == 0:
            for i in range(len(pmotionResult[j])):
                array.append(int(hex(ord(pmotionResult[j][i]))[2:], 16))
        else:
            array.append(int(pmotionResult[j], 16))
    return array



ser2 = serial.Serial('COM16', 115200)
while True:
    for i in range(12):
        print("正在开启相机......"+str(i))
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
        ret0, frame0 = video_photo0.read()
        cv2.imwrite(str(0+i*4) + '.jpg', frame0)
        print("上面拍照成功")
        video_photo0.release()
        # 拍照1###################################################################################

        # 拍照下###################################################################################
        ret1, frame1 = video_photo1.read()
        cv2.imwrite(str(1+i*4) + '.jpg', frame1)
        print("下面拍照成功")
        video_photo1.release()
        # 拍照2###################################################################################

        # 拍照左###################################################################################
        ret2, frame2 = video_photo2.read()
        cv2.imwrite(str(2+i*4) + '.jpg', frame2)
        print("左拍照成功")
        video_photo2.release()
        # 拍照3###################################################################################

        # 拍照右###################################################################################
        ret3, frame3 = video_photo3.read()
        cv2.imwrite(str(3+i*4) + '.jpg', frame3)
        print("右拍照成功")
        video_photo3.release()
        # 拍照4###################################################################################
        s= input("继续")
    s = input("本轮结束")


