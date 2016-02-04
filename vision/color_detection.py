from camera import Camera
from calibrate import step
from matplotlib import pyplot as plt
import numpy as np
import cv2


def nothing(x):
    pass

# HSV Colors
WHITE_LOWER = np.array([1, 0, 100])
WHITE_HIGHER = np.array([36, 255, 255])

BLUE_LOWER = np.array([90, 50, 50])
BLUE_HIGHER = np.array([130, 255, 255])

RED_LOWER = np.array([100, 160, 60])
RED_HIGHER = np.array([200, 255, 255])

'''
RED_LOWER = np.array([0, 240, 140])
RED_HIGHER = np.array([9, 255, 255])
'''
YELLOW_LOWER = np.array([9, 50, 50])
YELLOW_HIGHER = np.array([11, 255, 255])

c = Camera()
# create trackbars for color change
cv2.namedWindow('image')
cv2.createTrackbar('H low','image',0,360,nothing)
cv2.createTrackbar('S low','image',0,255,nothing)
cv2.createTrackbar('V low','image',0,255,nothing)
cv2.createTrackbar('H high','image',0,360,nothing)
cv2.createTrackbar('S high','image',0,255,nothing)
cv2.createTrackbar('V high','image',0,255,nothing)

while(1):

	frame = step(c.get_frame())

	blur = cv2.GaussianBlur(frame,(19,19), 0)
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

	# get current positions of four trackbars
	h_l = cv2.getTrackbarPos('H low','image')
	s_l = cv2.getTrackbarPos('S low','image')
	v_l = cv2.getTrackbarPos('V low','image')
	h_h = cv2.getTrackbarPos('H high','image')
	s_h = cv2.getTrackbarPos('S high','image')
	v_h = cv2.getTrackbarPos('V high','image')

	print "["+str(h_l)+","+str(s_l)+","+str(v_l)+"] ["+str(h_h)+","+str(s_h)+","+str(v_h)+"]" 
	low = np.array([h_l, s_l, v_l])
	high = np.array([h_h, s_h, v_l])

	mask = cv2.inRange(hsv, low, high)
	# mask = cv2.inRange(hsv, BLUE_LOWER, BLUE_HIGHER)
	ret,thresh = cv2.threshold(mask,127,255,0)

	_, contours, _ = cv2.findContours(thresh, 1, 2)
	# len(contours) represents the number of objects detected

	for i in range(0, len(contours)):
		cnt = contours[i]
		M = cv2.moments(cnt)
		if M['m00'] == 0 :
			continue

		# center coordinates:	
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

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