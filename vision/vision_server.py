#!/usr/bin/env python2.7
#
# This file is used to start up the vision server.
import zmq

from camera import Camera
from tracker import *

colors = {}
colors['yellow'] = (0,255,255)
colors['bright_blue'] = (255,255,0)
colors['pink'] = (127,0,255)
colors['green'] = (0,255,0)
colors['red'] = (0,0,255)
colors['blue'] = (255,0,0)

print "\nPossible team colors: yellow/bright_blue\n"
our_team_color = raw_input("Specify your team colour: ")
num_of_pink = raw_input("Specify the number of pink dots on your robot: ")
ball_color = raw_input("Specify ball color: ")

if int(num_of_pink) == 1:
	our_letters = 'GREEN'
	our_col = colors['green']
	our_robot_color = 'green_robot'
	mate_letters = 'PINK'
	mate_col = colors['pink']
	our_mate_color = 'pink_robot'
else:
	our_letters = 'PINK'
	our_col = colors['pink']
	our_robot_color = 'pink_robot'
	mate_letters = 'GREEN'
	mate_col = colors['green']
	our_mate_color = 'green_robot'


def main():
	# setup a pub server
	ctx = zmq.Context()
	s = ctx.socket(zmq.PUB)
	s.bind("tcp://*:5556")

	# vision setup/config
	c = Camera(port=1)

	our_robot = RobotTracker(our_team_color, int(num_of_pink))
  	ball = BallTracker(ball_color)

	while True:
		frame = c.get_frame()

		# get robot orientations
		ball_center = ball.getBallCoordinates(frame)
		our_orientation, our_robot_center = our_robot.getRobotOrientation(frame, 'us', our_robot_color)
		our_mate_orientation, our_mate_center = our_robot.getRobotOrientation(frame, 'us', our_mate_color)
		pink_opponent_orientation, pink_opponent_center = our_robot.getRobotOrientation(frame, 'opponent', 'pink_robot')
		green_opponent_orientation, green_opponent_center = our_robot.getRobotOrientation(frame, 'opponent', 'green_robot')

		s.send_pyobj({
			"ball_center": Tracker.transformCoordstoDecartes(ball_center),
			"our_robot_center": our_robot_center,
			"our_orientation": our_orientation
			})
		# return (Tracker.transformCoordstoDecartes(ball_center), our_robot_center, our_orientation[1])

if __name__ == "__main__":
	main()
