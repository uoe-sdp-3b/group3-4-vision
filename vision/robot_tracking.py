from tracker import *
from camera import Camera
import argparse
import time
import zmq


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",
                        help="Our Team Colour",
                        required=True,
                        choices=["yellow", "light_blue"])
    parser.add_argument("-d",
                        help="Number of dots",
                        required=True,
                        choices=["1", "3"])
    parser.add_argument("-b",
                        help="Ball Colour",
                        required=True,
                        choices=["red", "blue"])
    parser.add_argument("-c", help="Computer Name (useful for testing)")

    return parser.parse_args()


def main():
    # socket setup
    ctx = zmq.Context()
    socket = ctx.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    args = parse_args()
    c = Camera()

    frame = c.get_frame()

    colors = {}
    colors['yellow'] = (0, 255, 255)
    colors['light_blue'] = (255, 255, 0)
    colors['pink'] = (127, 0, 255)
    colors['green'] = (0, 255, 0)
    colors['red'] = (0, 0, 255)
    colors['blue'] = (255, 0, 0)

    our_team_color = args.t
    num_of_pink = args.d
    ball_color = args.b
    print("(%s, %s, %s)" % (our_team_color, num_of_pink, ball_color))

    # create our robot as object:
    our_robot = RobotTracker(our_team_color, int(num_of_pink), computer=args.c)
    ball = BallTracker(ball_color)

    # convert string colors into GBR
    our_circle_color = colors[our_team_color]
    if our_team_color == 'yellow':
        opponent_circle_color = colors['light_blue']
    else:
        opponent_circle_color = colors['yellow']

    # assign colors and names to the robots
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

    # main feed controller:
    while True:
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        frame = c.get_frame()

        # get robot orientations and centers, also get ball coordinates
        try:
            ball_center = ball.getBallCoordinates(frame)
            our_orientation, our_robot_center = our_robot.getRobotOrientation(
                frame, 'us', our_robot_color)
            our_mate_orientation, our_mate_center = our_robot.getRobotOrientation(
                frame, 'us', our_mate_color)
            pink_opponent_orientation, pink_opponent_center = our_robot.getRobotOrientation(
                frame, 'opponent', 'pink_robot')
            green_opponent_orientation, green_opponent_center = our_robot.getRobotOrientation(
                frame, 'opponent', 'green_robot')
        except ValueError:
            print("Exception calculating ball")
            ball_center = None
            our_orientation = None
            our_mate_orientation = None
            pink_opponent_orientation = None
            green_opponent_orientation = None

        if ball_center is not None:
            cv2.circle(frame, (int(ball_center[0]), int(ball_center[1])), 7,
                       colors[ball_color], 2)
            cv2.putText(frame, 'BALL',
                        (int(ball_center[0]) - 15, int(ball_center[1]) + 15),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5,
                        colors[ball_color])
        # draw circle  around robots:

        our_robot_center = None
        our_mate_center = None
        pink_opponent_center = None
        green_opponent_center = None
        if our_orientation is not None:
            _, v0 = our_orientation
            x0, y0 = our_robot_center
            vector0 = (x0 + v0[0] * 20, y0 + v0[1] * 20)
            x_0, y_0 = Tracker.transformCoordstoCV(vector0)
            our_robot_center = Tracker.transformCoordstoCV(our_robot_center)
            cv2.line(frame,
                     (int(our_robot_center[0]), int(our_robot_center[1])),
                     (int(x_0), int(y_0)), (0, 0, 255), 2)
            cv2.circle(frame,
                       (int(our_robot_center[0]),
                        int(our_robot_center[1])), 20, our_circle_color, 2)
            cv2.putText(frame, 'OUR', (int(our_robot_center[0]) - 15,
                                       int(our_robot_center[1]) + 30),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, our_col)
            cv2.putText(frame, our_letters, (int(our_robot_center[0]) - 20,
                                             int(our_robot_center[1]) + 40),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, our_col)

        if our_mate_orientation is not None:
            _, v1 = our_mate_orientation
            x1, y1 = our_mate_center
            vector1 = (x1 + v1[0] * 20, y1 + v1[1] * 20)
            x_1, y_1 = Tracker.transformCoordstoCV(vector1)
            our_mate_center = Tracker.transformCoordstoCV(our_mate_center)
            cv2.line(frame, (int(our_mate_center[0]), int(our_mate_center[1])),
                     (int(x_1), int(y_1)), (0, 0, 255), 2)
            cv2.circle(frame,
                       (int(our_mate_center[0]),
                        int(our_mate_center[1])), 20, our_circle_color, 2)
            cv2.putText(frame, mate_letters,
                        (int(our_mate_center[0]) - 15, int(our_mate_center[1])
                         + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, mate_col)
            cv2.putText(frame, 'TEAMMATE',
                        (int(our_mate_center[0]) - 30, int(our_mate_center[1])
                         + 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, mate_col)

        if pink_opponent_orientation is not None:
            _, v2 = pink_opponent_orientation
            x2, y2 = pink_opponent_center
            vector2 = (x2 + v2[0] * 20, y2 + v2[1] * 20)
            x_2, y_2 = Tracker.transformCoordstoCV(vector2)
            pink_opponent_center = Tracker.transformCoordstoCV(
                pink_opponent_center)
            cv2.line(frame, (int(pink_opponent_center[0]),
                             int(pink_opponent_center[1])),
                     (int(x_2), int(y_2)), (0, 0, 255), 2)
            cv2.circle(frame, (int(pink_opponent_center[0]),
                               int(pink_opponent_center[1])), 20,
                       opponent_circle_color, 2)
            cv2.putText(frame, 'PINK', (int(pink_opponent_center[0]) - 15,
                                        int(pink_opponent_center[1]) + 30),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (127, 0, 255))
            cv2.putText(frame, 'OPPONENT', (int(pink_opponent_center[0]) - 30,
                                            int(pink_opponent_center[1]) + 40),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (127, 0, 255))

        if green_opponent_orientation is not None:
            _, v3 = green_opponent_orientation
            x3, y3 = green_opponent_center
            vector3 = (x3 + v3[0] * 20, y3 + v3[1] * 20)
            x_3, y_3 = Tracker.transformCoordstoCV(vector3)
            green_opponent_center = Tracker.transformCoordstoCV(
                green_opponent_center)
            cv2.line(frame, (int(green_opponent_center[0]),
                             int(green_opponent_center[1])),
                     (int(x_3), int(y_3)), (0, 0, 255), 2)
            cv2.circle(frame, (int(green_opponent_center[0]),
                               int(green_opponent_center[1])), 20,
                       opponent_circle_color, 2)
            cv2.putText(frame, 'GREEN', (int(green_opponent_center[0]) - 15,
                                         int(green_opponent_center[1]) + 30),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 255, 0))
            cv2.putText(frame, 'OPPONENT',
                        (int(green_opponent_center[0]) - 30,
                         int(green_opponent_center[1]) + 40),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 255, 0))

        # sending of data down pipe
        socket.send_pyobj({
            "time": time.time(),
            "ball_center": ball_center,
            "us": {
                "orientation": our_orientation,
                "location": our_robot_center
            },
            "mate": {
                "orientation": our_mate_orientation,
                "location": our_mate_center
            },
            "pink_opponent": {
                "orientation": pink_opponent_orientation,
                "location": pink_opponent_center
            },
            "green_opponent": {
                "orientation": green_opponent_orientation,
                "location": green_opponent_center
            }
        })

        cv2.imshow('frame', frame)

    c.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
