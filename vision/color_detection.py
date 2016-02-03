from camera import Camera
from calibrate import step
from matplotlib import pyplot as plt
import numpy as np
import cv2

# HSV Colors
WHITE_LOWER = np.array([1, 0, 100])
WHITE_HIGHER = np.array([36, 255, 255])

BLUE_LOWER = np.array([95., 50., 50.])
BLUE_HIGHER = np.array([110., 255., 255.])

RED_LOWER = np.array([0, 240, 140])
RED_HIGHER = np.array([9, 255, 255])

YELLOW_LOWER = np.array([9, 50, 50])
YELLOW_HIGHER = np.array([11, 255, 255])

c = Camera()

lower_blue_b = 0
i = 0

while(1):

	frame = step(c.get_frame())

	blur = cv2.GaussianBlur(frame,(19,19), 0)
	#gray_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
	lower_blue = np.array([90,50,50])
	upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
	mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
	res = cv2.bitwise_and(frame,frame, mask= mask)
	cv2.imshow('hsv', hsv) 
	#cv2.imshow('blurred lines', blur)
	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask)
	cv2.imshow('res',res)
	
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

c.close() 
cv2.destroyAllWindows()       