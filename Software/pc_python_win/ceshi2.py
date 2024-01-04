import cv2
import numpy as np


video = cv2.VideoCapture(3)
ju = video.isOpened()
i = 0
while ju:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)
    # frame = white_balance(frame,5)
    cv2.imshow("frame", frame)
    keyword = cv2.waitKey(1)
    if keyword == ord('q'):
        break
    elif keyword == ord('s'):
        i += 1
        cv2.imwrite('4' + '.jpg', frame)

video.release()
cv2.destroyAllWindows()
