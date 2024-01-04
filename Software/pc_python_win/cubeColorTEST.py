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


def bubble(SK, k):  # 冒泡函数
    for i in range(len(SK)):
        for j in range(0, len(SK)-1-i):
            if SK[j][k] > SK[j+1][k]:
                SK[j], SK[j+1] = SK[j+1], SK[j]
    return SK


def color_know(hsv, cube_color_centre, face_name, color_name, i, j, k, num, C_A, C_B):  # 颜色识别函数
    # k=0识别左，1识别右 # 识别函数 #i为编号 j为面号 z为1靠近光源
    # 定义数组 0位存放编号，1位存放颜色

    if k == 0:
        cube_lump = [face_name[j] + str(i+1), 0]
    else:
        i += 9
        cube_lump = [face_name[j] + str(i+1-9), 0]
    hsv_color = [0, 0, 0]
    tmp = 0
    p = 400
    for l in range(20):
        for h in range(20):

            hsv_color1 = hsv[cube_color_centre[i]
                             [0]+h-10, cube_color_centre[i][1]+l-10]
            if hsv_color1[0] > 160 and hsv_color1[1] > 120:
                tmp += 1

            if (hsv_color1[1] < C_A[0][1] + 30) and p > 6:
                p -= 1
            elif (hsv_color1[2] < 110) and p > 6:
                p -= 1
            elif (hsv_color1[0] > 160) and p > 6:
                p -= 1
            else:
                """ if (j == 0 and k == 0 and i == 3):
                    print(hsv_color1[0], hsv_color1[1], hsv_color1[2]) """
                hsv_color[0] = hsv_color[0] + hsv_color1[0]
                hsv_color[1] = hsv_color[1] + hsv_color1[1]
                hsv_color[2] = hsv_color[2] + hsv_color1[2]

    hsv_color[0] = hsv_color[0] / p
    hsv_color[1] = hsv_color[1] / p
    hsv_color[2] = hsv_color[2] / p

    if C_B[4][0] > 160 and C_B[2][0] < 55:
        C_B[4] = C_B[3]
        C_B[3][0] = 75
        C_B[3][1] = 240
    NUM = 5
    print("----------------------------------------------------")
    print(hsv_color)
    print(C_B)
    # ['W','B','G','Y','O','R']

    if C_B[4][0] > 160:
        if (hsv_color[1] < C_A[1][1]) and (abs(hsv_color[1] - C_A[0][1]) < abs(hsv_color[1] - C_A[1][1])) and (hsv_color[0] > 60) or (hsv_color[1] < 53):
            cube_lump[1] = color_name[0]  # W
        elif (135 > hsv_color[0] > C_B[2][0]):
            if (abs(hsv_color[0] - C_B[3][0]) < abs(hsv_color[0] - C_B[2][0])):
                cube_lump[1] = color_name[1]  # B
            else:
                cube_lump[1] = color_name[2]  # G
        elif (135 > hsv_color[0] > C_B[1][0]):
            if (abs(hsv_color[0] - C_B[2][0]) < abs(hsv_color[0] - C_B[1][0])) and hsv_color[1] > 125:
                cube_lump[1] = color_name[2]  # G
            else:
                cube_lump[1] = color_name[3]  # Y
        elif (135 > hsv_color[0] > C_B[0][0]) and ((abs(hsv_color[0] - C_B[1][0]) < abs(hsv_color[0] - C_B[0][0])) and hsv_color[1] < 125):
            cube_lump[1] = color_name[3]  # Y
        else:
            if ((abs(hsv_color[0] - C_B[0][0]) < abs(hsv_color[0] - C_B[1][0])) and hsv_color[2] < 165) or (hsv_color[2] < 145)\
                    or (hsv_color[0] < C_B[0][0]):
                cube_lump[1] = color_name[5]  # R
            elif (abs(hsv_color[0] - C_B[1][0]) < abs(hsv_color[0] - C_B[0][0])) and hsv_color[2] > 170:
                cube_lump[1] = color_name[4]  # O
            elif (abs(hsv_color[1] - C_B[1][1]) < abs(hsv_color[1] - C_B[0][1])) or hsv_color[2] > 195:
                cube_lump[1] = color_name[4]  # O
            else:
                cube_lump[1] = color_name[5]  # R
    else:
        if ((hsv_color[1] < C_A[1][1]) and (abs(hsv_color[1] - C_A[0][1]) < abs(hsv_color[1] - C_A[1][1])) and (hsv_color[0] > 60)) or (hsv_color[1] < 53)\
            or (90 < hsv_color[0] < 110 and hsv_color[1] < C_A[1][1] ):
            cube_lump[1] = color_name[0]  # W
        elif (hsv_color[0] > C_B[3][0]):
            if (abs(hsv_color[0] - C_B[4][0]) < abs(hsv_color[0] - C_B[3][0])):
                cube_lump[1] = color_name[1]  # B
            else:
                cube_lump[1] = color_name[2]  # G
        elif (hsv_color[0] > C_B[2][0]):
            if (abs(hsv_color[0] - C_B[3][0]) < abs(hsv_color[0] - C_B[2][0])) and hsv_color[1] > 125:
                cube_lump[1] = color_name[2]  # G
            else:
                cube_lump[1] = color_name[3]  # Y
        elif C_B[2][0] - 5 < hsv_color[0] < C_B[2][0] + 5:
                cube_lump[1] = color_name[3]  # Y
        elif (hsv_color[0] > C_B[1][0]) and ((abs(hsv_color[0] - C_B[2][0]) < abs(hsv_color[0] - C_B[1][0])) and hsv_color[1] < 125):
            cube_lump[1] = color_name[3]  # Y
        else:
            if (abs(hsv_color[1] - C_B[1][1]) < abs(hsv_color[1] - C_B[0][1])) and hsv_color[2] > 195:
                cube_lump[1] = color_name[4]  # O
            elif 151>hsv_color[1] > 140 and (abs(hsv_color[0] - C_B[1][0]) < abs(hsv_color[0] - C_B[0][0])):
                cube_lump[1] = color_name[4]  # O
            elif C_B[0][0]>hsv_color[0] and hsv_color[2] < 150:
                cube_lump[1] = color_name[5]  # R
            elif ((abs(hsv_color[0] - C_B[0][0]) < abs(hsv_color[0] - C_B[1][0])) and hsv_color[2] < 165) or (hsv_color[2] < 145) \
                    or ((hsv_color[0] < C_B[0][0])and hsv_color[1] > C_B[1][1]):
                cube_lump[1] = color_name[5]  # R
            elif (abs(hsv_color[0] - C_B[1][0]) < abs(hsv_color[0] - C_B[0][0])) and hsv_color[2] > 170:
                cube_lump[1] = color_name[4]  # O
            elif (abs(hsv_color[1] - C_B[1][1]) < abs(hsv_color[1] - C_B[0][1])) or hsv_color[2] > 195:
                cube_lump[1] = color_name[4]  # O
            else:
                cube_lump[1] = color_name[5]  # R

    if p < 6:
        cube_lump[1] = color_name[0]
    if tmp >= 5 and hsv_color[2] <  120 or (hsv_color[0] > 145) :
        cube_lump[1] = color_name[5]# R
    if (12 <hsv_color[0] < 25) and (155 > hsv_color[1] > 130) and (hsv_color[2] > 210):
                cube_lump[1] = color_name[4]  # O
    elif (C_B[1][1] +6 > hsv_color[1] > C_B[1][1] -6) and ( hsv_color[0] < 18) and ( hsv_color[2] > 160):
                cube_lump[1] = color_name[4]  # O
    
    return cube_lump


def color_replace(k):  # 颜色替换函数
    # k表示中心面颜色
    global color_any
    # 遍历六个面
    for i in range(6):
        # 遍历每个面的九个色块
        for j in range(9):
            if color_any[i][j][1] == cube_mid_color[k][1]:  # 中心块[方向，颜色]
                color_any[i][j][1] = face_name[k]  # 替换


def cube_color_all(ColorThreshold_A, ColorThreshold_B):  # 色块识别函数
    # 第一面F
    print("第一面F")
    for i in range(9):
        test_f = color_know(
            hsv0, cube_FR, face_name, color_name, i, 2, 0, num, ColorThreshold_A, ColorThreshold_B)
        if i == 4:
            cube_mid_color[2] = test_f
        color_any[2][i] = test_f  # 将F面编号依据URFDLB顺序，存入数组第2位
    print(color_any[2])
    # 第二面R
    print("第二面R")
    for i in range(9):
        test_r = color_know(
            hsv0, cube_FR, face_name, color_name, i, 1, 1, num, ColorThreshold_A, ColorThreshold_B)
        if i == 4:
            cube_mid_color[1] = test_r
        color_any[1][i] = test_r
    print(color_any[1])
    # 第三面L
    print("第三面L")
    for i in range(9):
        test_l = color_know(
            hsv1, cube_LB, face_name, color_name, i, 4, 0, num, ColorThreshold_A, ColorThreshold_B)
        if i == 4:
            cube_mid_color[4] = test_l
        color_any[4][i] = test_l
    print(color_any[4])
    # 第四面U
    print("第四面U")
    for i in range(9):
        test_u = color_know(
            hsv3, cube_U, face_name, color_name, i, 0, 0, num, ColorThreshold_A, ColorThreshold_B)
        if i == 4:
            cube_mid_color[0] = test_u
        color_any[0][i] = test_u
    print(color_any[0])
    # 第五面D
    print("第五面D")
    for i in range(9):
        test_d = color_know(
            hsv2, cube_D, face_name, color_name, i, 3, 0, num, ColorThreshold_A, ColorThreshold_B)
        if i == 4:
            cube_mid_color[3] = test_d
        color_any[3][i] = test_d
    print(color_any[3])
    # 第六面B
    print("第六面B")
    for i in range(9):
        test_b = color_know(
            hsv1, cube_LB, face_name, color_name, i, 5, 1, num, ColorThreshold_A, ColorThreshold_B)
        if i == 4:
            cube_mid_color[5] = test_b
        color_any[5][i] = test_b
    print(color_any[5])


def color_detection(ar, num):  # 颜色检测函数
    ColorThreshold_A = []
    ColorThreshold_B = []
    color_name = ['W', 'B', 'G', 'Y', 'O', 'R']
    for k in range(6):
        tmp = 0
        for i in range(6):
            for j in range(9):
                if color_name[k] == ar[i][j][1]:
                    tmp += 1

        if tmp == 9:
            print("%s识别成功========================" % (color_name[k]))
        elif tmp > 9:
            RedSwitchOver[0] += 64
            ColorThreshold = kmeans_detection()
            ColorThreshold_A = ColorThreshold[np.argsort(ColorThreshold[:, 1])]
            ColorThreshold_B = ColorThreshold_A[1:]
            ColorThreshold_B = ColorThreshold_B[np.argsort(
                ColorThreshold_B[:, 0])]
            # print(ColorThreshold_A, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print(ColorThreshold_B, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            cube_color_all(ColorThreshold_A, ColorThreshold_B)
            ar = np.array(color_any)
            color_detection(ar, num)
        elif tmp < 9:
            RedSwitchOver[0] += 64
            ColorThreshold = kmeans_detection()
            ColorThreshold_A = ColorThreshold[np.argsort(ColorThreshold[:, 1])]
            ColorThreshold_B = ColorThreshold_A[1:]
            ColorThreshold_B = ColorThreshold_B[np.argsort(
                ColorThreshold_B[:, 0])]

            cube_color_all(ColorThreshold_A, ColorThreshold_B)
            ar = np.array(color_any)
            color_detection(ar, num)


def cube_color(PixelAarry, hsv_img, z):
    for k in range(len(PixelAarry)):
        """ if (z == 1):
            print("=============================") """
        for i in range(num):
            for j in range(num):
                """ if (z == 1):
                    print(hsv_img[[PixelAarry[k][1]+j-int(num/2)],
                                  [PixelAarry[k][0]+i-int(num/2)]][0][1]) """
                if 180 >= hsv_img[[PixelAarry[k][1]+j-int(num/2)], [PixelAarry[k][0]+i-int(num/2)]][0][0] > 160:
                    RedSwitchOff[0] += 1
                PixelHsvAarry.append(
                    [int(hsv_img[[PixelAarry[k][1]+j-int(num/2)], [PixelAarry[k][0]+i-int(num/2)]][0][0]),
                     int(hsv_img[[PixelAarry[k][1]+j -
                                  int(num/2)], [PixelAarry[k][0]+i-int(num/2)]][0][1])])


def cube_kmeans():
    hsv_img = np.array(PixelHsvAarry)

    kmeans = KMeans(
        n_clusters=RedSwitch[0], n_init=20)
    kmeans.fit(hsv_img)
    return kmeans.cluster_centers_


def kmeans_detection():

    if RedSwitchOff[0] > RedSwitchOver[0]:
        RedSwitch[0] = 7
    else:
        RedSwitch[0] = 6
    ColorThreshold = cube_kmeans()
    ColorThreshold_A = ColorThreshold[np.argsort(ColorThreshold[:, 1])]
    ColorThreshold_B = ColorThreshold_A[1:]
    ColorThreshold_B = ColorThreshold_B[np.argsort(ColorThreshold_B[:, 0])]
    return ColorThreshold


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


""" S = input('准备')
ser1 = serial.Serial('COM8', 115200)
ser1.write(calculate_crc16(
    ["RG3" + "LG3", "", ""]))
ser1.close() """
video_photo0 = cv2.VideoCapture(2) #上
video_photo1 = cv2.VideoCapture(4) #下
video_photo2 = cv2.VideoCapture(0) #左
video_photo3 = cv2.VideoCapture(3) #右

# 拍照上###################################################################################
S = input('开始')
ret0, frame0 = video_photo0.read()
cv2.imwrite(str(2) + '.jpg', frame0)
img0 = cv2.imread('2.jpg')  # 图片0,识别左F,右R
hsv0 = cv2.cvtColor(img0, cv2.COLOR_BGR2HSV)
print("上面拍照成功")
# 拍照1###################################################################################

# 拍照下###################################################################################
ret1, frame1 = video_photo1.read()
cv2.imwrite(str(1) + '.jpg', frame1)
img1 = cv2.imread('1.jpg')  # 图片2,识别左L,右B
hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
print("下面拍照成功")
# 拍照2###################################################################################

# 拍照左###################################################################################
ret2, frame2 = video_photo2.read()
cv2.imwrite(str(0) + '.jpg', frame2)
img2 = cv2.imread('0.jpg')  # 图片3,识别D
hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
print("左拍照成功")
# 拍照3###################################################################################

# 拍照右###################################################################################
ret3, frame3 = video_photo3.read()
cv2.imwrite(str(3) + '.jpg', frame3)
img3 = cv2.imread('3.jpg')  # 图片1,识别U
hsv3 = cv2.cvtColor(img3, cv2.COLOR_BGR2HSV)
print("右拍照成功")
# 拍照4###################################################################################

# 坐标上
PixelAarry_0 = [[190, 130], [250, 125], [320, 120],
                [190, 230], [240, 240], [305, 245],
                [185, 335], [240, 350], [315, 370],
                [410, 115], [485, 125], [545, 130],
                [400, 245], [480, 245], [545, 240],
                [405, 370], [480, 350], [545, 335]]
# 坐标下
PixelAarry_1 = [[250, 170], [265, 100], [270, 50],
                [350, 175], [350, 110], [355, 55],
                [455, 175], [445, 110], [440, 55],
                [255, 360], [255, 310], [250, 245],
                [345, 365], [350, 315], [350, 250],
                [430, 365], [445, 315], [455, 250]]

# 坐标左
PixelAarry_3 = [[135, 215], [225, 120], [315, 35],
                [215, 315], [315, 210], [410, 120],
                [325, 395], [420, 310], [500, 205],
                ]
# 坐标右
PixelAarry_2 = [[315, 390], [210, 300], [140, 190], [420, 295], [320, 200],  [230, 105], [495, 195], [410, 105], [315, 30],
                ]

for i in range(len(PixelAarry_0)):
    cv2.circle(img0, (PixelAarry_0[i][0],
               PixelAarry_0[i][1]), 2, (0, 0, 255), -1)
for i in range(len(PixelAarry_1)):
    cv2.circle(img1, (PixelAarry_1[i][0],
               PixelAarry_1[i][1]), 2, (0, 0, 255), -1)
for i in range(len(PixelAarry_2)):
    cv2.circle(img2, (PixelAarry_2[i][0],
               PixelAarry_2[i][1]), 2, (0, 0, 255), -1)
for i in range(len(PixelAarry_3)):
    cv2.circle(img3, (PixelAarry_3[i][0],
               PixelAarry_3[i][1]), 2, (0, 0, 255), -1)

cv2.imwrite('00.jpg', img0)
cv2.imwrite('22.jpg', img1)
cv2.imwrite('33.jpg', img2)
cv2.imwrite('11.jpg', img3)

PixelHsvAarry = []
RedSwitch = [0]
RedSwitchOff = [0]
RedSwitchOver = [0]
num = 10

cube_color(PixelAarry_0, hsv0, 1)
cube_color(PixelAarry_1, hsv1, 0)
cube_color(PixelAarry_2, hsv2, 0)
cube_color(PixelAarry_3, hsv3, 0)

if RedSwitchOff[0] > RedSwitchOver[0]:
    RedSwitch[0] = 7
else:
    RedSwitch[0] = 6
ColorThreshold = cube_kmeans()
ColorThreshold__A = ColorThreshold[np.argsort(ColorThreshold[:, 1])]
print(ColorThreshold__A)
ColorThreshold__B = ColorThreshold__A[1:]
ColorThreshold__B = ColorThreshold__B[np.argsort(ColorThreshold__B[:, 0])]
print(ColorThreshold__B)

S = input('开始3')
# 定义原始数组存放54个编号 FRLUDB
color_any = [[[], [], [], [], [], [], [], [], []],
             [[], [], [], [], [], [], [], [], []],
             [[], [], [], [], [], [], [], [], []],
             [[], [], [], [], [], [], [], [], []],
             [[], [], [], [], [], [], [], [], []],
             [[], [], [], [], [], [], [], [], []]]
# 定义字符串存放发送kociemba.solve('')
cube_solve = ''
# 定义数组存放魔方中心块颜色
cube_mid_color = [[], [], [], [], [], []]
# 定义数组存放颜色名
color_name = ['W', 'B', 'G', 'Y', 'O', 'R']
# 定义数组存放方向名
face_name = ['U', 'R', 'F', 'D', 'L', 'B']
num = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]


# F,R
cube_FR = [[y, x] for x, y in PixelAarry_0]
# L,B
cube_LB = [[y, x] for x, y in PixelAarry_1]
# D
cube_D = [[y, x] for x, y in PixelAarry_3]
# U
cube_U = [[y, x] for x, y in PixelAarry_2]

cube_color_all(ColorThreshold__A, ColorThreshold__B)
# 所有颜色识别完毕得到 一个三维数组color_any[[[编号，颜色],[],[]],[[],[]],[[],[]]] 以及 cube_color_name = []
ar = np.array(color_any)
print(ar)
color_detection(ar, num)  # 颜色检测
print(RedSwitchOver[0])
ar = np.array(color_any)
for k in range(6):
    ar[np.where(ar == cube_mid_color[k][1])] = face_name[k] + "*"
for i in range(6):
    for j in range(9):
        cube_solve += ar[i][j][1]
rt = str(cube_solve).replace('*', '')

print(rt)
# 动作解析###################################################################################
motionResult = kociemba.solve(rt)


# 最初解法200步  #单字符表示顺90，‘表示逆90 ，2表示180
print("**************Kociemba动作**************")
print(motionResult)
motionResult = motion_optimal_one(motionResult + " " + " " + " " + " ")
motionResult = motion_optimal_three(motionResult)
# 优化动作
print("****************优化动作****************")
motionResult = calculate_crc16(
    ["RG1" + "LG1" + motion_optimal_three(motionResult) + "RG0" + "LG0", "", ""])


S = input('开始复原')
ser2 = serial.Serial('COM16', 115200)
ser2.write(motionResult)
ser2.close()

