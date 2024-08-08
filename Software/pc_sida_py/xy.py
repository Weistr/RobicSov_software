import cv2
import kociemba
import socket
import time
import numpy as np


# 定义鼠标交互函数
def mouseColor(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('HSV:', hsv[y, x])  # 输出图像坐标(x,y)处的HSV的�?
        print('坐标:', [x, y])


dst_white = cv2.imread('0.jpg')  # 读进来是BGR格式
hsv = cv2.cvtColor(dst_white, cv2.COLOR_BGR2HSV)  # 变成HSV格式
cv2.namedWindow("Color Picker")
cv2.setMouseCallback("Color Picker", mouseColor)
cv2.imshow("Color Picker", dst_white)

while True:
    keyword = cv2.waitKey(1)
    if keyword == ord('q'):
        break

cv2.destroyAllWindows()
