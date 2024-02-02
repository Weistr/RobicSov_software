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

def calculate_crc16(motionResult):  # CRC校验
    # sarray=发送数组
    data = motionResult[0]
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
    motionResult[2] = crc[0]+crc[1]
    motionResult[1] = crc[2]+crc[3]
    print("CRC16校验值为:", crc)
    print(motionResult)

    array = []
    for j in range(len(motionResult)):
        if j == 0:
            for i in range(len(motionResult[j])):
                array.append(int(hex(ord(motionResult[j][i]))[2:], 16))
        else:
            array.append(int(motionResult[j], 16))
    return array


def cv_show(name, img):  # 显示函数
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def video_takephoto(i):  # 拍照函数
    # i为第几张图
    video_photo = cv2.VideoCapture(i)
    """ time.sleep(1) """
    # 获得一帧图片
    ret, frame = video_photo.read()
    # frame = cv2.flip(frame, 1)
    # cv2.imshow("video",frame)
    cv2.imwrite(str(i) + '.jpg', frame)
    # 读取图像
    img = cv2.imread(str(i) + '.jpg')
    cv2.imwrite(str(i) + '.jpg', img)




def cube_color(PixelPosXy, hsv_img, z):
    for k in range(len(PixelPosXy)):
        for i in range(num):
            for j in range(num):
                PixelHsvAarry.append(
                    [int(hsv_img[[PixelPosXy[k][1]+j-int(num/2)], [PixelPosXy[k][0]+i-int(num/2)]][0][0]),
                     int(hsv_img[[PixelPosXy[k][1]+j -int(num/2)], [PixelPosXy[k][0]+i-int(num/2)]][0][1])
                     ]
                    )
                PixelVAarry.append(
                    int(hsv_img[[PixelPosXy[k][1]+j-int(num/2)], [PixelPosXy[k][0]+i-int(num/2)]][0][2])
                    )
                


def motion_optimal_three(motionResult):  # 动作优化函数thr
    array = ['LW0', 'LW2', 'LW1', 'LW3', 'LW4', 'LW5', 'LW6', 'LG1', 'LG2', '',
             'RW0', 'RW2', 'RW1', 'RW3', 'RW4', 'RW5', 'RW6', 'RG1', 'RG2',]
    motionNowResult = ""
    for i in range(len(motionResult)):
        for j in range(len(array)):
            if motionResult[i] == j:
                motionResult[i] = array[j]
        motionNowResult += str(motionResult[i])
    return motionNowResult


def motor_angle(angle, motion, i):  # 3逆180 4顺180 5逆270 6顺270 # i判断左右手
    angleMotion = [[10, 11, 12, 13, 14, 15, 16, 17, 18], [
        0, 1, 2, 3, 4, 5, 6, 7, 8]]
    if angle >= 0:
        if angle == 0:  # 当前角度
            if motion == 1:  # 动作
                return angleMotion[i][1]
            elif motion == 2:  # 动作
                return angleMotion[i][2]
            elif motion == 3:  # 动作
                return angleMotion[i][3]
        elif angle == 90:
            if motion == 1:
                return angleMotion[i][4]
            elif motion == 2:
                return angleMotion[i][0]
            elif motion == 3:
                return angleMotion[i][2]
        elif angle == 180:
            if motion == 1:
                return angleMotion[i][6]
            elif motion == 2:
                return angleMotion[i][1]
            elif motion == 3:
                return angleMotion[i][0]
        elif angle == 270:
            if motion == 1:
                return angleMotion[i][0]
            elif motion == 2:
                return angleMotion[i][4]
            elif motion == 3:
                return angleMotion[i][1]
    if angle < 0:
        if angle == -90:
            if motion == 1:
                return angleMotion[i][0]
            elif motion == 2:
                return angleMotion[i][3]
            elif motion == 3:
                return angleMotion[i][1]
        elif angle == -180:
            if motion == 1:
                return angleMotion[i][2]
            elif motion == 2:
                return angleMotion[i][5]
            elif motion == 3:
                return angleMotion[i][0]
        elif angle == -270:
            if motion == 1:
                return angleMotion[i][3]
            elif motion == 3:
                return angleMotion[i][2]
            elif motion == 2:
                return angleMotion[i][0]


def motion_optimal_three(motionResult):  # 动作优化函数thr
    array = ['LW0', 'LW1', 'LW2', 'LW4', 'LW3', 'LW6', 'LW5', 'LG1', 'LG2', '',
             'RW0', 'RW1', 'RW2', 'RW4', 'RW3', 'RW6', 'RW5', 'RG1', 'RG2',]
    motionNowResult = ""
    for i in range(len(motionResult)):
        for j in range(len(array)):
            if motionResult[i] == j:
                motionResult[i] = array[j]
        motionNowResult += str(motionResult[i])
    return motionNowResult


def motor_angle(angle, motion, i):  # 3逆180 4顺180 5逆270 6顺270 # i判断左右手
    angleMotion = [[10, 11, 12, 13, 14, 15, 16, 17, 18], [
        0, 1, 2, 3, 4, 5, 6, 7, 8]]
    if angle >= 0:
        if angle == 0:  # 当前角度
            if motion == 1:  # 动作
                return angleMotion[i][1]
            elif motion == 2:  # 动作
                return angleMotion[i][2]
            elif motion == 3:  # 动作
                return angleMotion[i][3]
        elif angle == 90:
            if motion == 1:
                return angleMotion[i][4]
            elif motion == 2:
                return angleMotion[i][0]
            elif motion == 3:
                return angleMotion[i][2]
        elif angle == 180:
            if motion == 1:
                return angleMotion[i][6]
            elif motion == 2:
                return angleMotion[i][1]
            elif motion == 3:
                return angleMotion[i][0]
        elif angle == 270:
            if motion == 1:
                return angleMotion[i][0]
            elif motion == 2:
                return angleMotion[i][4]
            elif motion == 3:
                return angleMotion[i][1]
    if angle < 0:
        if angle == -90:
            if motion == 1:
                return angleMotion[i][0]
            elif motion == 2:
                return angleMotion[i][3]
            elif motion == 3:
                return angleMotion[i][1]
        elif angle == -180:
            if motion == 1:
                return angleMotion[i][2]
            elif motion == 2:
                return angleMotion[i][5]
            elif motion == 3:
                return angleMotion[i][0]
        elif angle == -270:
            if motion == 1:
                return angleMotion[i][3]
            elif motion == 3:
                return angleMotion[i][2]
            elif motion == 2:
                return angleMotion[i][0]


def motion_optimal_one(motionResult):  # 动作优化函数one
    angleL = 0
    angleR = 0
    oldState = ['U', 'R', 'F', 'D', 'L', 'B']  # 传入初始解法
    newState = ['U', 'R', 'F', 'D', 'L', 'B']
    motionNewResult = []
    for i in range(len(motionResult)):
        # 魔方无复位#######################################################################################################
        if motionResult[i] == oldState[0]:  # U
            if (motionResult[i+2] in [oldState[1], oldState[5], oldState[3]]) or \
                    (motionResult[i+3] in [oldState[1], oldState[5], oldState[3]]) or (i+2 < len(motionResult)):  # 左转右换
                if angleL in [0, 180, -180] and angleR in [0, 180, -180]:  # 状态一左平右平
                    if angleR in [0, 180]:
                        R = motor_angle(angleR, 1, 0)
                        angleR += 90
                        motionNewResult += [8, R, 7]
                        R = motor_angle(angleR, 2, 0)
                        angleR -= 90
                        motionNewResult += [18, R, 17]
                    else:
                        angleR += 90
                        motionNewResult += [8, 12, 7]
                        angleR += 90
                        motionNewResult += [18, 10, 17]

                elif angleL in [0, 180, -180] and angleR in [90, 270, -90, -270]:  # 状态二左平右竖
                    R = motor_angle(angleR, 1, 0)
                    if angleR == 270:
                        angleR = 0
                    else:
                        angleR += 90
                    motionNewResult += [8, R, 7]

                elif angleL in [90, 270, -90, -270] and angleR in [0, 180, -180]:
                    # 状态三左竖右平
                    if angleL in [90, -90]:
                        angleL = 0
                        motionNewResult += [8, 0, 7]
                    elif angleL == 270:
                        angleL -= 90
                        motionNewResult += [8, 4, 7]
                    elif angleL == -270:
                        angleL += 90
                        motionNewResult += [8, 3, 7]

                    if angleR in [0, 180]:
                        R = motor_angle(angleR, 1, 0)
                        angleR += 90
                        motionNewResult += [8, R, 7]
                        R = motor_angle(angleR, 2, 0)
                        angleR -= 90
                        motionNewResult += [18, R, 17]
                    else:
                        angleR += 90
                        motionNewResult += [8, 12, 7]
                        angleR += 90
                        motionNewResult += [18, 10, 17]

                if motionResult[i+1] == "2":
                    L = motor_angle(angleL, 3, 1)
                    if angleL == 0:
                        angleL = -180
                    else:
                        angleL = 0
                    motionNewResult += [L]
                elif motionResult[i+1] == "'":
                    L = motor_angle(angleL, 2, 1)
                    angleL -= 90
                    motionNewResult += [L]
                else:
                    L = motor_angle(angleL, 1, 1)
                    angleL += 90
                    motionNewResult += [L]
                newState[0] = oldState[1]
                newState[1] = oldState[3]
                newState[3] = oldState[4]
                newState[4] = oldState[0]

            elif (motionResult[i+2] in [oldState[2], oldState[4]]) or \
                    (motionResult[i+3] in [oldState[2], oldState[4]]):  # 右转左换
                if angleL in [0, 180, -180] and angleR in [0, 180, -180]:
                    # 状态一左平右平
                    if angleL in [0, -180]:
                        L = motor_angle(angleL, 2, 1)
                        angleL -= 90
                        motionNewResult += [18, L, 17]
                        L = motor_angle(angleL, 1, 1)
                        angleL += 90
                        motionNewResult += [8, L, 7]
                    else:
                        angleL -= 90
                        motionNewResult += [18, 1, 17]
                        motionNewResult += [8, 0, 7]

                elif angleL in [0, 180, -180] and angleR in [90, 270, -90, -270]:
                    # 状态二左平右竖
                    if angleR in [90, -90]:
                        angleR = 0
                        motionNewResult += [18, 10, 17]
                    elif angleR == 270:
                        angleR -= 90
                        motionNewResult += [18, 14, 17]
                    elif angleR == -270:
                        angleR += 90
                        motionNewResult += [18, 13, 17]

                    if angleL in [0, -180]:
                        L = motor_angle(angleL, 2, 1)
                        angleL -= 90
                        motionNewResult += [18, L, 17]
                        L = motor_angle(angleL, 1, 1)
                        angleL += 90
                        motionNewResult += [8, L, 7]
                    else:
                        angleL -= 90
                        motionNewResult += [18, 1, 17]
                        angleL -= 90
                        motionNewResult += [8, 0, 7]

                elif angleL in [90, 270, -90, -270] and angleR in [0, 180, -180]:
                    # 状态三左竖右平
                    L = motor_angle(angleL, 2, 1)
                    if angleL == -270:
                        angleL = 0
                    else:
                        angleL -= 90
                    print(angleL, i)
                    motionNewResult += [18, L, 17]

                if motionResult[i+1] == "2":
                    R = motor_angle(angleR, 3, 0)
                    if angleR == 0:
                        angleR = -180
                    else:
                        angleR = 0
                    motionNewResult += [R]
                elif motionResult[i+1] == "'":
                    R = motor_angle(angleR, 2, 0)
                    angleR -= 90
                    motionNewResult += [R]
                else:
                    R = motor_angle(angleR, 1, 0)
                    angleR += 90
                    motionNewResult += [R]
                newState[0] = oldState[2]
                newState[2] = oldState[3]
                newState[3] = oldState[5]
                newState[5] = oldState[0]
            else:
                print("UUUUUU")
        elif motionResult[i] == oldState[1]:  # R 左转右换
            # 状态一左平右平
            if angleL in [0, 180, -180] and angleR in [0, 180, -180]:
                R = motor_angle(angleR, 3, 0)
                if angleR == 0:
                    angleR -= 180
                else:
                    angleR = 0
                motionNewResult += [8, R, 7]
            elif angleL in [0, 180, -180] and angleR in [90, 270, -90, -270]:
                # 状态二左平右竖
                if angleR in [90, 270]:
                    R = motor_angle(angleR, 3, 0)
                    angleR -= 180
                else:
                    R = motor_angle(angleR, 3, 0)
                    angleR += 180
                motionNewResult += [8, R, 7]
                motionNewResult += [18, 10, 17]
                angleR = 0
            elif angleL in [90, 270, -90, -270] and angleR in [0, 180, -180]:
                # 状态三左竖右平
                if angleL in [90, 270]:
                    L = motor_angle(angleL, 2, 1)
                    angleL -= 90
                    motionNewResult += [8, L, 7]
                else:
                    L = motor_angle(angleL, 1, 1)
                    angleL += 90
                    motionNewResult += [8, L, 7]
                R = motor_angle(angleR, 3, 0)
                if angleR == 0:
                    angleR = -180
                else:
                    angleR = 0
                motionNewResult += [8, R, 7]
            else:
                print("RRRRRR")
            if motionResult[i+1] == "2":
                L = motor_angle(angleL, 3, 1)
                if angleL == 0:
                    angleL = -180
                else:
                    angleL = 0
                motionNewResult += [L]
            elif motionResult[i+1] == "'":
                L = motor_angle(angleL, 2, 1)
                angleL -= 90
                motionNewResult += [L]
            else:
                L = motor_angle(angleL, 1, 1)
                angleL += 90
                motionNewResult += [L]
            newState[0] = oldState[3]
            newState[1] = oldState[4]
            newState[3] = oldState[0]
            newState[4] = oldState[1]
        elif motionResult[i] == oldState[2]:  # F 右转左换
            if angleL in [0, 180, -180] and angleR in [0, 180, -180]:
                # 状态一左平右平
                L = motor_angle(angleL, 3, 1)
                if angleL == 0:
                    angleL -= 180
                else:
                    angleL = 0
                motionNewResult += [18, L, 17]
            elif angleL in [0, 180, -180] and angleR in [90, 270, -90, -270]:
                # 状态二左平右竖
                if angleR in [90,  270]:
                    R = motor_angle(angleR, 2, 0)
                    angleR -= 90
                else:
                    R = motor_angle(angleR, 1, 0)
                    angleR += 90
                motionNewResult += [18, R, 17]
                L = motor_angle(angleL, 3, 1)
                if angleL == 0:
                    angleL -= 180
                else:
                    angleL = 0
                motionNewResult += [18, L, 17]
            elif angleL in [90, 270, -90, -270] and angleR in [0, 180, -180]:
                # 状态三左竖右平
                if angleL in [90, 270]:
                    L = motor_angle(angleL, 3, 1)
                    angleL -= 180
                else:
                    L = motor_angle(angleL, 3, 1)
                    angleL += 180
                motionNewResult += [18, L, 17]
                motionNewResult += [8, 0, 7]
                angleL = 0
            else:
                print("FFFFFFF")
            if motionResult[i+1] == "2":
                R = motor_angle(angleR, 3, 0)
                if angleR == 0:
                    angleR = -180
                else:
                    angleR = 0
                motionNewResult += [R]
            elif motionResult[i+1] == "'":
                R = motor_angle(angleR, 2, 0)
                angleR -= 90
                motionNewResult += [R]
            else:
                R = motor_angle(angleR, 1, 0)
                angleR += 90
                motionNewResult += [R]

            newState[0] = oldState[3]
            newState[2] = oldState[5]
            newState[3] = oldState[0]
            newState[5] = oldState[2]
        elif motionResult[i] == oldState[3]:  # D
            if (motionResult[i+2] in [oldState[1], oldState[5], oldState[0]]) or \
                    (motionResult[i+3] in [oldState[1], oldState[5], oldState[0]]) or (i+2 < len(motionResult)):  # 左转右换
                if angleL in [0, 180, -180] and angleR in [0, 180, -180]:
                    # 状态一左平右平
                    if angleR in [0, -180]:
                        R = motor_angle(angleR, 2, 0)
                        angleR -= 90
                        motionNewResult += [8, R, 7]
                        R = motor_angle(angleR, 1, 0)
                        angleR += 90
                        motionNewResult += [18, R, 17]
                    else:
                        angleR -= 90
                        motionNewResult += [8, 11, 7]
                        angleR -= 90
                        motionNewResult += [18, 10, 17]
                elif angleL in [0, 180, -180] and angleR in [90, 270, -90, -270]:
                    # 状态二左平右竖
                    R = motor_angle(angleR, 2, 0)
                    if angleR == -270:
                        angleR = 0
                    else:
                        angleR -= 90
                    motionNewResult += [8, R, 7]
                elif angleL in [90, 270, -90, -270] and angleR in [0, 180, -180]:
                    # 状态三左竖右平
                    if angleL in [90, -90]:
                        angleL = 0
                        motionNewResult += [8, 0, 7]
                    elif angleL == 270:
                        angleL -= 90
                        motionNewResult += [8, 4, 7]
                    elif angleL == -270:
                        angleL += 90
                        motionNewResult += [8, 3, 7]

                    if angleR in [0, -180]:
                        R = motor_angle(angleR, 2, 0)
                        angleR -= 90
                        motionNewResult += [8, R, 7]
                        R = motor_angle(angleR, 1, 0)
                        angleR += 90
                        motionNewResult += [18, R, 17]
                    else:
                        angleR -= 90
                        motionNewResult += [8, 11, 7]
                        angleR -= 90
                        motionNewResult += [18, 10, 17]
                if motionResult[i+1] == "2":
                    L = motor_angle(angleL, 3, 1)
                    if angleL == 0:
                        angleL = -180

                    else:
                        angleL = 0
                    motionNewResult += [L]
                elif motionResult[i+1] == "'":
                    L = motor_angle(angleL, 2, 1)
                    angleL -= 90
                    motionNewResult += [L]
                else:
                    L = motor_angle(angleL, 1, 1)
                    angleL += 90

                    motionNewResult += [L]
                newState[0] = oldState[4]
                newState[1] = oldState[0]
                newState[3] = oldState[1]
                newState[4] = oldState[3]
            elif (motionResult[i+2] in [oldState[2], oldState[4]]) or \
                    (motionResult[i+3] in [oldState[2], oldState[4]]):  # 右转左换
                if angleL in [0, 180, -180] and angleR in [0, 180, -180]:
                    # 状态一左平右平
                    if angleL in [0, 180]:
                        L = motor_angle(angleL, 1, 1)
                        angleL += 90
                        motionNewResult += [18, L, 17]
                        L = motor_angle(angleL, 2, 1)
                        angleL -= 90
                        motionNewResult += [8, L, 7]
                    else:
                        angleL += 90
                        motionNewResult += [18, 2, 17]
                        angleL += 90
                        motionNewResult += [8, 0, 7]
                elif angleL in [0, 180, -180] and angleR in [90, 270, -90, -270]:
                    # 状态二左平右竖
                    if angleR in [90, -90]:
                        angleR = 0
                        motionNewResult += [18, 10, 17]
                    elif angleR == 270:
                        angleR -= 90
                        motionNewResult += [18, 14, 17]
                    elif angleR == -270:
                        angleR += 90
                        motionNewResult += [18, 13, 17]

                    if angleL in [0, 180]:
                        L = motor_angle(angleL, 1, 1)
                        angleL += 90
                        motionNewResult += [18, L, 17]
                        L = motor_angle(angleL, 2, 1)
                        angleL -= 90
                        motionNewResult += [8, L, 7]
                    else:
                        angleL += 90
                        motionNewResult += [18, 2, 17]
                        angleL += 90
                        motionNewResult += [8, 0, 7]
                elif angleL in [90, 270, -90, -270] and angleR in [0, 180, -180]:
                    # 状态三左竖右平
                    L = motor_angle(angleL, 1, 1)
                    if angleL == 270:
                        angleL = 0
                    else:
                        angleL += 90
                    motionNewResult += [18, L, 17]
                if motionResult[i+1] == "2":
                    R = motor_angle(angleR, 3, 0)
                    if angleR == 0:
                        angleR = -180
                    else:
                        angleR = 0
                    motionNewResult += [R]
                elif motionResult[i+1] == "'":
                    R = motor_angle(angleR, 2, 0)
                    angleR -= 90
                    print(angleR, i)
                    motionNewResult += [R]
                else:
                    R = motor_angle(angleR, 1, 0)
                    angleR += 90
                    motionNewResult += [R]

                newState[0] = oldState[5]
                newState[2] = oldState[0]
                newState[3] = oldState[2]
                newState[5] = oldState[3]
            else:
                print("DDDDDDDD")
        elif motionResult[i] == oldState[4]:  # L 左转
            if angleL in [0, 180, -180] and angleR in [90, 270, -90, -270]:
                # 状态二左平右竖
                if angleR in [90, 270]:
                    R = motor_angle(angleR, 2, 0)
                    angleR -= 90
                    motionNewResult += [18, R, 17]
                else:
                    R = motor_angle(angleR, 1, 0)
                    angleR += 90
                    motionNewResult += [18, R, 17]
            else:
                print("LLLLLLLLL")
            if motionResult[i+1] == "2":
                L = motor_angle(angleL, 3, 1)
                if angleL == 0:
                    angleL = -180
                else:
                    angleL = 0
                motionNewResult += [L]
            elif motionResult[i+1] == "'":
                L = motor_angle(angleL, 2, 1)
                angleL -= 90

                motionNewResult += [L]
            else:
                L = motor_angle(angleL, 1, 1)
                angleL += 90

                motionNewResult += [L]
        elif motionResult[i] == oldState[5]:  # B 右转
            if angleL in [90, 270, -90, -270] and angleR in [0, 180, -180]:  # 状态三左竖右平
                if angleL in [90,  270]:
                    L = motor_angle(angleL, 2, 1)
                    angleL -= 90
                    motionNewResult += [8, L, 7]
                else:
                    L = motor_angle(angleL, 1, 1)
                    angleL += 90
                    motionNewResult += [8, L, 7]

            if motionResult[i+1] == "2":
                R = motor_angle(angleR, 3, 0)
                if angleR == 0:
                    angleR = -180
                else:
                    angleR = 0
                motionNewResult += [R]
            elif motionResult[i+1] == "'":
                R = motor_angle(angleR, 2, 0)
                angleR -= 90
                motionNewResult += [R]
            else:
                R = motor_angle(angleR, 1, 0)
                angleR += 90

                motionNewResult += [R]

        oldState = newState.copy()

    motionResult = motionNewResult

    for i in range(len(motionResult)):
        # 优化手指空夹#######################################################################################################
        if (motionResult[i] == 7 and motionResult[i+1] == 8) or (motionResult[i] == 17 and motionResult[i+1] == 18):
            motionResult[i] = 99
            motionResult[i+1] = 99
    motionResult = list(filter(lambda x: x != 99, motionResult))
    print("***************总电机动作***************")
    print(motionResult)
    return motionResult

def colorDec_Up(hs,thes,h):
    if hs[1] < thes[7]:
        return 'w'
    elif thes[0] <= hs[0] < thes[2] and h<thes[8]:
        return 'r'
    elif thes[0] < hs[0] < thes[2] and h>thes[8]:
        return 'o'
    elif thes[2] < hs[0] < thes[3] :
        return 'y'
    elif thes[3] < hs[0] < thes[4]:
        return 'g'
    elif thes[4] < hs[0] < thes[5]:
        return 'b'
    elif thes[5] < hs[0] < thes[6]:
        return 'r'
    else :
        return 'n'
    
def colorDec_Down(hs,thes,h):
    if hs[1] < thes[7]:
        return 'w'
    elif thes[0] <= hs[0] <= thes[2] and h<thes[8]:
        return 'r'
    elif thes[0] <= hs[0] < thes[2] and h>thes[8]:
        return 'o'
    elif thes[2] < hs[0] < thes[3]:
        return 'y'
    elif thes[3] < hs[0] < thes[4]:
        return 'g'
    elif thes[4] < hs[0] < thes[5]:
        return 'b'
    elif thes[5] < hs[0] < thes[6]:
        return 'r'
    else :
        return 'n'
    

def colorDec_LR(hs,thes,h):
    if hs[1] < thes[7]:
        return 'w'
    elif thes[0] <= hs[0] <= thes[1] and h<thes[8]:
        return 'r'
    elif thes[0] <= hs[0] < thes[1] and h>thes[8]:
        return 'o'
    elif thes[1] < hs[0] < thes[2]:
        return 'y'
    elif thes[2] < hs[0] < thes[3]:
        return 'g'
    elif thes[3] < hs[0] < thes[4]:
        return 'b'
    else :
        return 'n'
    
def colorDec_Hole3(hs,thes,h):
    if thes[0] < hs[0] < thes[1] and h < thes[5]:
        return 'r'
    elif thes[0] < hs[0] < thes[1] and h > thes[5]:
        return 'o'
    elif thes[1] < hs[0] < thes[2] and hs[1] > thes[6] :
        return 'y'
    elif thes[1] < hs[0] < thes[2] and hs[1] < thes[6] :
        return 'w'
    elif thes[2] < hs[0] < thes[3] :
        return 'g'
    elif thes[3] < hs[0] < thes[4] :
        return 'b'
    else :
        return 'n'
    
def colorDec_Hole2(hs,thes,h):
    if thes[0] <= hs[0] <= thes[1] and h < thes[5]:
        return 'r'
    elif thes[0] <= hs[0] <= thes[1] and h > thes[5]:
        return 'o'
    elif thes[1] < hs[0] < thes[2] and hs[1] > thes[6] :
        return 'y'
    elif thes[1] < hs[0] < thes[2] and hs[1] < thes[6] :
        return 'w'
    elif thes[2] < hs[0] < thes[3] :
        return 'g'
    elif thes[3] < hs[0] < thes[4] :
        return 'b'
    else :
        return 'n'

while True:
    video_photo0 = cv2.VideoCapture(1) #上
    video_photo1 = cv2.VideoCapture(4) #下
    video_photo2 = cv2.VideoCapture(3) #
    video_photo3 = cv2.VideoCapture(2) #
    flag = 0
    # 拍照上###################################################################################
    if flag==1 :
        flag = 0
        for i in range(50)
        if(motionResult[i]=='W'):
            
        S = input('请拿下魔方，按回车复位手爪')


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
    # 拍照4###################################################################################
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

    for i in range(len(PixelPosXy_0)):
        cv2.circle(img0, (PixelPosXy_0[i][0],
                PixelPosXy_0[i][1]), 2, (0, 0, 255), -1)
    for i in range(len(PixelPosXy_1)):
        cv2.circle(img1, (PixelPosXy_1[i][0],
                PixelPosXy_1[i][1]), 2, (0, 0, 255), -1)
    for i in range(len(PixelPosXy_2)):
        cv2.circle(img2, (PixelPosXy_2[i][0],
                PixelPosXy_2[i][1]), 2, (0, 0, 255), -1)
    for i in range(len(PixelPosXy_3)):
        cv2.circle(img3, (PixelPosXy_3[i][0],
                PixelPosXy_3[i][1]), 2, (0, 0, 255), -1)

    cv2.imwrite('00.jpg', img0)
    cv2.imwrite('11.jpg', img1)
    cv2.imwrite('22.jpg', img2)
    cv2.imwrite('33.jpg', img3)

    PixelHsvAarry = []
    PixelVAarry = []
    RedSwitch = [0]
    RedSwitchOff = [0]
    RedSwitchOver = [0]
    num = 3

    cube_color(PixelPosXy_0, hsv0, 1)
    cube_color(PixelPosXy_1, hsv1, 0)
    cube_color(PixelPosXy_2, hsv2, 0)
    cube_color(PixelPosXy_3, hsv3, 0)


    print("**************avr**************")
    #求平均值
    #[H, S]
    cube_color_avr = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],
                    [0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],
                    [0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],
                    [0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],
                    [0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],
                    [0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]
                    ]
    cube_v_avr =[0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                ]

    #2维数组，54个blob,8个为阈值. 其中前7个为H值区间:红橙黄绿蓝红，8个为S值用于分辨白色,9用于红(为v值)
    #hole3: r,o区间,y,w区间,g区间,b区间,ro_v, yw_s
    #hole2 r,o区间,y,w区间,g区间,b区间,ro_v, yw_s
    CubeColorThreshold = [
                    #F面
                    [-5,3,10,60,90,155,180,75,150],[-5,3,10,60,90,155,180,75,150],[-5,3,10,60,90,155,180,75,150],
                    [-5,3,10,60,90,155,180,75,150],[-5,3,10,60,90,155,180,75,150],[-5,3,10,60,90,155,180,75,150],
                    [-5,3,10,60,90,155,180,75,150],[-5,3,10,60,90,155,180,75,150],[-5,3,10,60,90,155,180,75,150],

                    #R面
                    [-3,3,10,60,90,155,180,75,150],[-3,3,10,60,90,155,180,75,150],[-3,3,10,60,90,155,180,75,150],
                    [-3,3,10,60,90,155,180,75,150],[-3,3,10,60,90,155,180,75,150],[-3,3,10,60,90,155,180,75,150],
                    [-3,3,10,60,90,155,180,75,150],[-3,3,10,60,90,155,180,75,150],[-3,3,10,60,90,155,180,75,150],

                    #L面 同
                    [-7,1,10,60,90,155,180,55,152],[-7,1,10,60,90,155,180,55,152],[-7,1,10,60,90,155,180,55,140],
                    [-7,1,10,60,90,155,180,55,152],[-7,1,10,60,90,155,180,55,152],[-7,1,10,60,90,155,180,55,152],
                    [-7,1,10,60,90,155,180,55,152],[-7,1,10,60,90,155,180,55,152],[-7,1,10,60,90,155,180,55,152],

                    #B面    t同[1,106](o)
                    [-7,1,10,60,90,155,180,40,152],[-7,1,10,60,90,155,180,55,152],[-7,1,10,60,90,155,180,55,152],
                    [-7,1,10,60,90,155,180,40,152],[-7,1,10,60,90,155,180,55,152],[-7,1,10,60,90,155,180,55,152],
                    [-7,1,10,60,90,155,180,40,152],[-7,1,10,60,90,155,180,55,152],[-7,1,10,60,90,155,180,55,152],

                    #D面 同
                    [-9,8,57,85,155,155,180,60,125],[-9,8,57,85,155,155,180,60,125],[-9,8,57,85,155,155,180,60,140],
                    [-9,6,40,90,120,55,90,55,125],[-9,8,57,85,155,155,180,80,125],[-9,8,57,85,155,155,180,90,125],
                    [-9,8,57,85,155,155,180,90,125],[-9,6,40,90,120,55,90,90,125],[-9,8,57,85,155,155,180,90,125],

                    #U面 同
                    [-9,8,57,85,155,155,180,90,125],[-9,3,57,82,120,55,110,55,125],[-9,8,57,85,155,155,180,90,125],
                    [-9,3,57,82,120,55,110,55,125],[-9,8,57,85,155,155,180,90,125],[-9,8,57,85,155,155,180,90,125],
                    [-9,8,57,85,155,155,180,90,125],[-9,8,57,85,155,155,180,90,125],[-9,8,57,85,155,155,180,90,125],

                    ]
    #球平均值
    for blob in range(54):
        for pix in range(9):
            if PixelHsvAarry[blob*9+pix][0] > 170 :
                PixelHsvAarry[blob*9+pix][0] -= 180
            cube_color_avr[blob][0] += PixelHsvAarry[blob*9+pix][0]
            cube_color_avr[blob][1] += PixelHsvAarry[blob*9+pix][1]
            cube_v_avr[blob] = int(PixelVAarry[blob*9+pix]) + int(cube_v_avr[blob])
        cube_color_avr[blob][0] = cube_color_avr[blob][0]//9
        cube_color_avr[blob][1] = cube_color_avr[blob][1]//9
        cube_v_avr[blob] = cube_v_avr[blob]//9

    print(cube_color_avr)

    #FR面中心块
    #cubeCenterBlobeColor[0] = colorDec_Up(cube_color_avr[4+0*9],CubeColorThreshold[4+0*9])

    #判断颜色
    cubeBlobeColor=[0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                ]
    cubeBlobeKociemba=[0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                ]
    for blob in range(54):
        if blob < 18 :#FR面
            cubeBlobeColor[blob] = colorDec_Up(cube_color_avr[blob],CubeColorThreshold[blob],cube_v_avr[blob])
        elif 18 <= blob < 36:#LB面
            cubeBlobeColor[blob] = colorDec_Down(cube_color_avr[blob],CubeColorThreshold[blob],cube_v_avr[blob])
        elif 36 <= blob < 45:#L/R面(D)
            if blob == 39 or blob==43:
                cubeBlobeColor[blob] = colorDec_Hole2(cube_color_avr[blob],CubeColorThreshold[blob],cube_v_avr[blob])
            else :
                cubeBlobeColor[blob] = colorDec_LR(cube_color_avr[blob],CubeColorThreshold[blob],cube_v_avr[blob])
        else:#L/R面（U）
            if blob == 46 or blob==48:
                cubeBlobeColor[blob] = colorDec_Hole3(cube_color_avr[blob],CubeColorThreshold[blob],cube_v_avr[blob])
            else :
                cubeBlobeColor[blob] = colorDec_LR(cube_color_avr[blob],CubeColorThreshold[blob],cube_v_avr[blob])
    #整理顺序
    cubeBlobeKociemba[0:9] = cubeBlobeColor[45:54]#U
    cubeBlobeKociemba[9:18] = cubeBlobeColor[9:18]#R
    cubeBlobeKociemba[18:27] = cubeBlobeColor[0:9]#F
    cubeBlobeKociemba[27:36] = cubeBlobeColor[36:45]#D
    cubeBlobeKociemba[36:45] = cubeBlobeColor[18:27]#L
    cubeBlobeKociemba[45:54] = cubeBlobeColor[27:36]#B
    #t替换色字符为面字符
    #判断中心块颜色,URFDLB
    cubeCenterBlobeColor=[0,0,0,0,0,0]
    print("**************cubeSortcolor**************")
    print(cubeBlobeKociemba)       
    cubeDef = ['U','R','F','D','L','B']
    for i in range(6):
        cubeCenterBlobeColor[i] = cubeBlobeKociemba[4+9*i]
    for i in range(54):
        for j in range(6):
            if cubeBlobeKociemba[i] == cubeCenterBlobeColor[j]:
                cubeBlobeKociemba[i] = cubeDef[j]

    kociembaInput = ''.join(cubeBlobeKociemba)
    print("**************cubecolor**************")
    print(cubeBlobeColor)

    print("**************cubeKociemba**************")
    print(kociembaInput)
    print("**************center**************")
    print(cubeCenterBlobeColor)
    print("**************raw**************")
    print(cube_color_avr)
    print("**************v**************")
    print(cube_v_avr)
    motionResult = kociemba.solve(kociembaInput)
    print("**************Kociemba动作**************")
    print(motionResult)
    # 动作解析###################################################################################
    # 最初解法200步  #单字符表示顺90，‘表示逆90 ，2表示180
    motionResult = motion_optimal_one(motionResult + " " + " " + " " + " ")
    motionResult = motion_optimal_three(motionResult)
    # 优化动作
    print("****************机器人动作****************")
    motionResult = calculate_crc16(
        ["RG1" + "LG1" + motion_optimal_three(motionResult) + "RG0" + "LG0", "", ""])
    #print(motionResult)
    S = input('开始复原')
    ser2 = serial.Serial('COM16', 115200)
    ser2.write(motionResult)
    ser2.close()
    flag = 1

