from camera import Camera
from calibrate import step
from matplotlib import pyplot as plt
from socket import gethostname
import numpy as np
import cv2
import math
from tools import *
from algebra import *

adjustments = {}
adjustments['blur'] = (11,11) # needs to be parametrized .. TODO
color_range = get_colors() #for PITHC=0

class Tracker():

    def denoiseMask(self, mask):
        kernel =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        po = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        po = cv2.morphologyEx(po, cv2.MORPH_OPEN, kernel)
        return po

    def getContours(self, frame, color, adjustments):

        blur_intensity = adjustments['blur']
        blurred_frame = cv2.GaussianBlur(frame, blur_intensity, 0)
        hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        if color == 'red':
            red_mask = cv2.inRange(hsv_frame, color_range['red']['min'], color_range['red']['max'])
            maroon_mask = cv2.inRange(hsv_frame, color_range['maroon']['min'], color_range['maroon']['max'])
            mask = cv2.bitwise_or(red_mask, maroon_mask)
        else:
            mask = cv2.inRange(hsv_frame, color_range[color]['min'], color_range[color]['max'])

        _, threshold = cv2.threshold(self.denoiseMask(mask), 127, 255, 0)

        _, contours, _ = cv2.findContours(threshold, 1, 2)

        return self.removeUselessContours(contours)

    def removeUselessContours( self, contours ) :
        if contours is None:
            return None
        real_contours = []
        for contour in contours:
            _, radius = cv2.minEnclosingCircle(contour)
            if radius > 1.3 and radius < 20:
                real_contours.append(contour)

        return real_contours

    # Extracts a center from a single contour
    def getContourCenter(self, contour):
        if contour is None:
            return None
        center, _ = cv2.minEnclosingCircle(contour)
        return center


    # Extracts the centers of a list of contours
    def getContourCenters(self, contours):

        return [ self.getContourCenter(x) for x in contours ]


    def getKFurthestContours(self, k, p, contours):

        distances = [ self.distance( p, self.getContourCenter(c) ) for c in contours ]
        distances_sorted = np.argsort(distances)
        return [ contours[x] for x in distances_sorted[-k:] ]


    def getKClosestContours(self, k, p, contours):

        distances = [ self.distance( p, self.getContourCenter(c) ) for c in contours ]
        distances_sorted = np.argsort(distances)

        return [ contours[x] for x in distances_sorted[:k]]


    # Gives us the contour with the biggest area from a list of contours
    def getBiggestContour(self, contours):

        max_area = -1
        max_contour_position = -1

        if len(contours) == 0:
            return None

        for i in range(0, len(contours)):
            area = cv2.contourArea(contours[i])
            if area > max_area:
                max_area = area
                max_contour_position = i

        return contours[max_contour_position]



class BallTracker(Tracker):

    def __init__(self, ball_color):
        self.color = ball_color


    # Extracts the ( center, radius ) of our ball
    def getBallCoordinates(self, frame):

        contours = self.getContours(frame, self.color, adjustments)
        if contours is None:
            return None
        ball_contour = self.getBiggestContour(contours)

        return self.getContourCenter(ball_contour)


class RobotTracker(Tracker):

    def __init__(self, ally_color='yellow'):

        self.ally_color = ally_color
        self.side_identifiers = ['yellow', 'bright_blue']


    def getAllRobots(self, frame):

        pink_contours = self.getContours(frame, 'pink', adjustments)
        green_contours = self.getContours(frame, 'green', adjustments)

        robots = {}
        for side_color in self.side_identifiers:
            side_contours = self.getContours(frame, side_color, adjustments)
            side_robots = getRobotCoordinates(self, side_contours, pink_contours)
            if( side_color == self.ally_color ):
                robots['ally'] = side_robots
            else :
                robots['enemy'] = side_robots

        for side, side_robs in robots.iteritems():
            for color, robot in side_robs.iteritems():
                center = robots[side][color].center
                orientation = getRobotOrientation(genter, green_contours, pink_contours, side)
                robots[side][color].orientation = orientation

            return robots


    def getRobotCoordinates(self, side_contours, pink_contours):

        side_robots = {'green' : None, 'pink' : None}
        for contour in side_contours:

            contour_center = self.getContourCenter(contour)
            pink_contour_count = 0

            for pink_contour in pink_contours:
                pink_contour_center = self.getContourCenter(pink_contour)

                dist = distance( pink_contour_center, contour_center )

                if dist < 20*20 :
                    pink_contour_count += 1

            if pink_contour_count == 1:
                side_robots['green'] = Robot(contour_center, None)
            elif pink_contour_count == 3:
                side_robots['pink'] = Robot(contour_center, None)

        return side_robots


    def getRobotOrientation(self, center, green_contours, pink_contours, group_color):

        magnitude = 30

        if center is None:
            return None, None

        if group_color == 'pink':

            green_contours = self.getContours(frame, 'green', adjustments)
            pink_contours = self.getContours(frame, 'pink', adjustments)

            if green_contours == []:
                return None, None

            orientation_green = self.getKClosestContours(1, center, green_contours)

            green_center = self.getContourCenter(orientation_green[0])

            orientation_pink = self.getKClosestContours(3, green_center, pink_contours)
            orientation_pink = self.getKFurthestContours(2, green_center, orientation_pink)
            if len(orientation_pink) != 2:
                return None, None

            pink_centers = self.getContourCenters(orientation_pink)
            mean_pink_point = meanPoint(pink_centers)

            center = transformCoordstoDecartes( center )
            mean_pink_point = transformCoordstoDecartes( mean_pink_point )
            direction_vector = getDirectionVector(center, mean_pink_point, magnitude)

            angle_radians = np.arctan2( direction_vector[1], direction_vector[0] )
            angle_degrees = math.degrees( angle_radians )

        else:

            pink_contours = self.getContours(frame, 'pink', adjustments)
            orientation_pink = self.getKClosestContours(1, center, pink_contours)

            if orientation_pink == []:
                return None, None

            pink_center = self.getContourCenter(orientation_pink[0])

            center = transformCoordstoDecartes(center)
            pink_center = transformCoordstoDecartes( pink_center )

            direction_vector = getDirectionVector( center, pink_center, magnitude )
            direction_vector = rotateVector( direction_vector, math.radians(215) )

            angle_radians = np.arctan2( direction_vector[1], direction_vector[0] )
            angle_degrees = math.degrees(angle_radians)

        return (angle_degrees, direction_vector), center
