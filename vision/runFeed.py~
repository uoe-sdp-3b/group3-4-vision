import sys
#sys.path.insert(0, '../')
from camera import Camera
from calibrate import step
import math
from matplotlib import pyplot as plt
import numpy as np
import cv2

from socket import gethostname
from colorsHSV import *
computer_name = gethostname().split('.')[0]

c = Camera()

while(1):

	frame = c.get_frame()
	cv2.imshow('frame',frame)

	
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.imwrite('example_img.png', frame)

c.close() 
cv2.destroyAllWindows()       
