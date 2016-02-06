import sys
sys.path.insert(0, '/afs/inf.ed.ac.uk/user/s12/s1237357/Desktop/group3-4-vision/vision')
sys.path.insert(0, '/afs/inf.ed.ac.uk/user/s12/s1237357/Desktop/group3-4-vision/vision/config')
from camera import Camera
from calibrate import step
import math
from matplotlib import pyplot as plt
import numpy as np
import cv2


def nothing(x):
    pass

# HSV Colors
WHITE_LOWER = np.array([1, 0, 100])
WHITE_HIGHER = np.array([36, 255, 255])

BLUE_LOWER = np.array([70, 50, 50])
BLUE_HIGHER = np.array([160, 255, 255])

BRIGHT_BLUE_LOWER = np.array([80, 80, 80])
BRIGHT_BLUE_HIGHER = np.array([100, 255, 255])

PINK_LOWER = np.array([145, 90, 90]) 
PINK_HIGHER = np.array([170, 255, 255])

RED_LOWER = np.array([0, 130, 110]) 
RED_HIGHER = np.array([7, 255, 255])
'''
#TODO: test these values
RED_LOWER = np.array([160, 150, 110]) 
RED_HIGHER = np.array([180, 255, 255])
'''
GREEN_LOWER = np.array([60, 110, 110])
GREEN_HIGHER = np.array([75, 255, 255])

BRIGHT_GREEN_LOWER = np.array([40, 140, 180])
BRIGHT_GREEN_HIGHER = np.array([55, 255, 255])

YELLOW_LOWER = np.array([25, 100, 100])
YELLOW_HIGHER = np.array([40, 255, 255])

c = Camera()
num_of_pink_dots = 0;
while(1):

	frame = step(c.get_frame())

	blur = cv2.GaussianBlur(frame,(11,11), 0)

	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

	yellow_mask = cv2.inRange(hsv, YELLOW_LOWER, YELLOW_HIGHER)
	pink_mask = cv2.inRange(hsv, PINK_LOWER, PINK_HIGHER)
	green_mask = cv2.inRange(hsv, BRIGHT_GREEN_LOWER, BRIGHT_GREEN_HIGHER)
	bright_blue_mask = cv2.inRange(hsv, BRIGHT_BLUE_LOWER, BRIGHT_BLUE_HIGHER)

	yellow_ret, yellow_thresh = cv2.threshold(yellow_mask,127,255,cv2.THRESH_BINARY)
	pink_ret, pink_thresh = cv2.threshold(pink_mask,127,255,cv2.THRESH_BINARY)
	green_ret, green_thresh = cv2.threshold(green_mask,127,255,cv2.THRESH_BINARY)
	_, bright_blue_thresh = cv2.threshold(bright_blue_mask,127,255,cv2.THRESH_BINARY)

	_, yellow_contours, _ = cv2.findContours(yellow_thresh, 1, 2)
	_, pink_contours, _ = cv2.findContours(pink_thresh, 1, 2)
	_, green_contours, _ = cv2.findContours(green_thresh, 1, 2)
	_, bright_blue_contours, _ = cv2.findContours(bright_blue_thresh, 1, 2)
	
	pink_balls = []
	#green_balls = []

	for i in range(0, len(pink_contours)):
		cnt = pink_contours[i]
		M = cv2.moments(cnt)
		if M['m00'] == 0 :
			continue

		# center coordinates:	
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		(x,y),radius = cv2.minEnclosingCircle(cnt)

		center = (int(x),int(y))
		pink_balls.append(center)
		radius = int(radius)
		cv2.circle(frame,center,radius,(0,0,255),2)
	'''	
	for i in range(0, len(green_contours)):
		cnt = green_contours[i]
		M = cv2.moments(cnt)
		if M['m00'] == 0 :
			continue

		# center coordinates:	
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		(x,y),radius = cv2.minEnclosingCircle(cnt)

		center = (int(x),int(y))
		green_balls.append(center)
		#print pink_balls
		radius = int(radius)
		cv2.circle(frame,center,radius,(0,255,0),2)
	'''	
	for i in range(0, len(bright_blue_contours)):
		cnt = bright_blue_contours[i]
		M = cv2.moments(cnt)
		if M['m00'] == 0 :
			continue

		# center coordinates:	
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		(x,y),radius = cv2.minEnclosingCircle(cnt)

		center = (int(x),int(y))
		radius = int(radius)
		cv2.circle(frame,center,radius,(255,255,0),2)

	for i in range(0, len(yellow_contours)):
		cnt = yellow_contours[i]
		M = cv2.moments(cnt)
		if M['m00'] == 0 :
			continue

		# center coordinates:	
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		'''
		print "-----------------------"
		#---------this is for detecting top plate-----------
		x,y,w,h = cv2.boundingRect(cnt)
		print x, y, w, h
		#yellow_mask = cv2.rectangle(yellow_mask,(x,y),(100,100),(0,255,0),2)
		rect = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		#mask = cv2.drawContours(mask,[box],0,(0,0,255),2)
		cv2.rectangle(frame, (x-10,y-10),(x+w+5,y+h+5),(0,255,0),2)
		'''
		num_of_pink = 0
		(x,y),radius = cv2.minEnclosingCircle(cnt)

		for i in range(0, len(pink_balls)):
			if (math.sqrt(((x-pink_balls[i][0])**2)+(y-pink_balls[i][1])**2) < 15):
				num_of_pink += 1

		center = (int(x),int(y))
		radius = int(radius)
		if num_of_pink == 3:
			cv2.putText(frame,'OUR',(center[0]-15, center[1]+30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, 90)
			cv2.putText(frame,'DEFENDER',(center[0]-30, center[1]+40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, 90)
		if num_of_pink == 1:
			cv2.putText(frame,'OUR',(center[0]-15, center[1]+30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, 220)
			cv2.putText(frame,'ATTACKER',(center[0]-30, center[1]+40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, 220)
		cv2.circle(frame,center,15,(0,255,255),2)	

	
		
    # Bitwise-AND mask  and original image
	#res = cv2.bitwise_and(frame,frame, mask= mask)
	cv2.imshow('hsv', hsv) 
	cv2.imshow('blurred lines', blur)
	cv2.imshow('frame',frame)
	cv2.imwrite('a2.png', frame)
	cv2.imwrite('b.png', frame)
	#cv2.imshow('mask',mask)
	#cv2.imshow('res',res)
	
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

c.close() 
cv2.destroyAllWindows()       