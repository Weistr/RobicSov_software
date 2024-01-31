import cv2

# 读取图片
img =cv2.imread('2.jpg')

# 将图片转化为HSV格式
hsv_img =cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 显示原始图片和HSV图片
cv2.imshow('Original Image', img)
cv2.imshow('HSV Image', hsv_img)

# 等待按下任意键退出窗口
cv2.waitKey(0)
cv2.destroyAllWindows()

