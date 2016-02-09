#from tracker import *
#from camera import Camera
import numpy as np
from numpy.linalg import inv

c = Camera()

t = BallTracker('red')

frame = c.get_frame()
ballpos = t.getBallCoordinates(frame)

previous_positions =  np.array( [ ballpos ] )

k = 10

def linear_regression( points ):
	num_pts = len(points)
	xc = points[:, [0]]
	yc = points[:, [1]]
	ones = np.ones((num_pts,1))
	X = np.concatenate((ones, xc), axis = 1)

	X_intermediary = np.dot(X.T, X)
	Y_intermediary = np.dot(X.T, yc)
	print X_intermediary
	print Y_intermediary

	R = np.dot( inv(X_intermediary), Y_intermediary )
	
	k = R[1][0]
	last_2 = points[-2:]
	first_x = last_2[0]
	second_x = last_2[1]
	if first_x < second_x :
		return [1, k]
	else :
		return [-1, -k]

def round_point( (x, y) ):
	return ( int(x), int(y) )

def add_points( (x1, y1), (x2, y2) ):
	return ( x1 + x2, y1 + y2 )

while True:

	frame = c.get_frame()
	ballpos = t.getBallCoordinates(frame)

	previous_positions = np.append(previous_positions, ballpos)

	last_k_positions = previous_positions[-k:]

	direction_vector = linear_regression(last_k_positions)
	direction_vector = [ 20 * x for x in direction_vector ]

	frame = cv2.circle(frame, round_point(ballpos), 20, (0,0,0), 2)
	cv2.line(frame, round_point(ballpos), round_point(add_points(ballpos, direction_vector)), (0,255,122), 2)

	cv2.imshow('frame', frame)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

c.close()
cv2.destroyAllWindows()