from tracker import *
from camera import Camera

c = Camera()

frame = c.get_frame()

t = BallTracker('red')

'''while True:
	frame = c.get_frame()
	center, radius = t.get_ball_coordinates(frame)
	print center

	frame = cv2.circle(frame, center, 8, (0,0,0), 2)

	cv2.imshow('frame', frame)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break
'''

r = RobotTracker('bright_blue', 3)

while True:
	frame = c.get_frame()
	center, radius = r.our_defender_coordinates(frame)
	#print center

	p = r.get_robot_orientation(frame, 'us', 'defender')
	print p

	print 80 * '='

	frame = cv2.circle(frame, center, 20, (0,0,0), 2)

	cv2.imshow('frame', frame)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break
