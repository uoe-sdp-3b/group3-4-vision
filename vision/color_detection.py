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
	#frame = cv2.imread('useful.png')

	blur = cv2.GaussianBlur(frame,(19,19), 0)
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
	lower_blue = np.array([90,50,50])
	upper_blue = np.array([130,255,255])

	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	ret,thresh = cv2.threshold(mask,127,255,0)

	_, contours, _ = cv2.findContours(thresh, 1, 2)

	for i in range(0, len(contours)):
		cnt = contours[i]
		M = cv2.moments(cnt)

		if M['m00'] == 0 :
			continue
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		print "X: "+str(cx)+"   Y: "+str(cy)+"\n"
		(x,y),radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		radius = int(radius)
		cv2.circle(frame,center,radius,(0,255,0),2)

    # Bitwise-AND mask and original image
	res = cv2.bitwise_and(frame,frame, mask= mask)
	cv2.imshow('hsv', hsv) 
	cv2.imshow('blurred lines', blur)
	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask)
	cv2.imshow('res',res)
	
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

c.close() 
cv2.destroyAllWindows()       