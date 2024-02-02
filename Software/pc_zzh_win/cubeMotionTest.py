import kociemba
import time
import numpy as np
import matplotlib.pyplot as plt

import skimage
from skimage import draw
from skimage import morphology
from skimage import data

from copy import deepcopy
from copy import deepcopy

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


motionResult = kociemba.solve("BBURUDBFUFFFRRFUUFLULUFUDLRRDBBDBDBLUDDFLLRRBRLLLBRDDF")
# 最初解法200步  #单字符表示顺90，‘表示逆90 ，2表示180
print("**************Kociemba动作**************")
print(motionResult)
motionResult = motion_optimal_one(motionResult + " " + " " + " " + " ")
motionResult = motion_optimal_three(motionResult)
# 优化动作
print("****************优化动作****************")
motionResult = calculate_crc16(
    ["RG1" + "LG1" + motion_optimal_three(motionResult) + "RG0" + "LG0", "", ""])
print(motionResult)