import numpy as np
import cv2
import math
from tools import *
from algebra import *
from array_queue import ArrayQueue

adjustments = {}
adjustments['blur'] = (11, 11)  # needs to be parametrized .. TODO
color_range = get_colors()  # for PITCH=0


class Tracker():
    def denoiseMask(self, mask):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        po = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        po = cv2.morphologyEx(po, cv2.MORPH_OPEN, kernel)
        return po

    def getContours(self, frame, color, adjustments):

        color_range = get_colors()
        blur_intensity = adjustments['blur']
        blurred_frame = cv2.GaussianBlur(frame, blur_intensity, 0)
        hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        if color == 'red':
            red_mask = cv2.inRange(hsv_frame, color_range['red']['min'],
                                   color_range['red']['max'])
            maroon_mask = cv2.inRange(hsv_frame, color_range['maroon']['min'],
                                      color_range['maroon']['max'])
            mask = cv2.bitwise_or(red_mask, maroon_mask)
        else:
            mask = cv2.inRange(hsv_frame, color_range[color]['min'],
                               color_range[color]['max'])

        _, threshold = cv2.threshold(self.denoiseMask(mask), 127, 255, 0)

        _, contours, _ = cv2.findContours(threshold, 1, 2)

        return self.removeUselessContours(contours)


    def getMultiColorContours(self, frame, color_list):
        all_contours = []
        for color in color_list:
            tmp_contours = self.getContours(frame, color, adjustments)

            # Gets the (CENTER, color) of the contours, not the list of contour object
            processed_contours = [(x, color) for x in self.getContourCenters(tmp_contours)]
            all_contours += processed_contours

        return all_contours

    def removeUselessContours(self, contours):
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
        print center
        return center

    # Extracts the centers of a list of contours
    def getContourCenters(self, contours):

        return [self.getContourCenter(x) for x in contours]

    def getKFurthestContours(self, k, p, contours):

        distances = [distance(p, self.getContourCenter(c)) for c in contours]
        distances_sorted = np.argsort(distances)
        return [contours[x] for x in distances_sorted[-k:]]

    def getKClosestContours(self, k, p, contours):

        distances = [distance(p, self.getContourCenter(c)) for c in contours]
        distances_sorted = np.argsort(distances)

        return [contours[x] for x in distances_sorted[:k]]

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
        if contours == []:
            return None
        ball_contour = self.getBiggestContour(contours)

        return transformCoordstoDecartes(self.getContourCenter(ball_contour))


class RobotTracker(Tracker):
    def __init__(self, ally_color='yellow', max_queue_size=20):

        self.ally_color = ally_color
        self.side_identifiers = ['yellow', 'bright_blue']
        self.robot_identifiers = ['pink', 'green']
        self.all_colors = self.side_identifiers + self.robot_identifiers
        self.opposing_color = {'yellow':'bright_blue', 'bright_blue':'yellow', 'pink':'green', 'green':'pink'}
        self.previous_locations = {}
        combinations = self.identifierCombinations()
        for c in combinations:
            previous_locations[c] = ArrayQueue(max_queue_size)



    def identifierCombinations(self):
        tmp = ['ally', 'enemy']
        combinations = [ (x,y) for x in tmp for y in self.robot_identifiers]
        return combinations

    def groupContours(self,contour_list):

        buckets = []
        for i in range(4):
            buckets.append([])

        l = len(contour_list)
        processed = [False] * l

        bucket_counter = 0
        for i in range(l):
            print "Koj kurac: ", bucket_counter
            center, color = contour_list[i]
            if color in self.side_identifiers:
                buckets[bucket_counter].append( (center, color) )
                print "USAO: ", color
                processed[i] = True
                for j in range(l):
                    if i == j:
                        continue
                    if processed[j]:
                        continue

                    support_center, support_color = contour_list[j]
                    dist = distance(center, support_center)
                    if dist < 20 * 20:
                        buckets[bucket_counter].append( (support_center, support_color) )
                        processed[j] = True

                bucket_counter += 1

        for i in range(l):
            if processed[i]:
                continue
            print "USAO"

            center, color = contour_list[i]
            buckets[bucket_counter].append( (center, color) )
            for j in range(l):
                if i == j:
                    continue
                if processed[j]:
                    continue

                support_center, support_color = contour_list[j]
                dist = distance(center, support_center)
                if dist < 30 * 30:
                    buckets[bucket_counter].append( (support_center, support_color) )
                    processed[j] = True

            bucket_counter += 1

        return (buckets, bucket_counter)


    def classifyBuckets(self, buckets):
        combinations = [(x, y) for x in self.side_identifiers for y in self.robot_identifiers]
        possibilities = [combinations] * 4

        print combinations
        bucket_classifications = [None] * 4

        # Elimination of bad classifications
        changed = True
        while changed:
            changed = False
            for i in range(4):
                num = {}
                for color in self.all_colors:
                    num[color] = len([x for (_, x) in buckets[i] if x == color])
                print "Robot -------> ", i
                print num

                for side_color in self.side_identifiers:
                    if num[side_color] == 1:
                        print "Enter"
                        opposing_col = self.opposing_color[side_color]
                        print "Pre-change: ", possibilities[i]
                        possibilities[i] = [ (a,b) for (a,b) in possibilities[i] if a != opposing_col ]
                        print "Post-change: ", possibilities[i]

                for robot_color in self.robot_identifiers:
                    if num[robot_color] > 1:
                        opposing_col = self.opposing_color[robot_color]
                        possibilities[i] = [ (a,b) for (a,b) in possibilities[i] if b != opposing_col ]

                print ""

            for i in range(4):
                if bucket_classifications[i] is not None:
                    continue

                pos_len = len(possibilities[i])
                if pos_len == 0:
                    print "Bucketing is fucked up"
                elif pos_len == 1:
                    # This is the case that we want
                    classification = possibilities[i][0]
                    bucket_classifications[i] = classification
                    for j in range(4):
                        possibilities[j] = [x for x in possibilities[j] if x != classification]

                    changed = True

        return bucket_classifications


    def gradientDescent(bucket):
        pass

    def calculateLocation(self, classification, bucket):

        # Can only happen if >= 2 contours in the bucket

        for center, color in bucket:
            if color in self.side_identifiers:
                return center

        return gradientDescent(bucket)


    def estimatePositions(self, buckets, bucket_classifications, num_buckets):

        color_map = {}
        color_map[ally_color] = 'ally'
        color_map[self.opposing_color[ally_color]] = 'enemy'


        combinations = self.identifierCombinations()
        estimated_locations = {}
        for c in combinations:
            estimated_locations[c] = None

        ''' Fill the estimated_locations where we can for sure'''
        for i in range(num_buckets):
            color_classification = bucket_classifications[i]
            real_classification = (color_map(color_classification[0]), color_classification[1])
            if classification is None:
                continue
            if len(buckets[i]) <= 1:
                continue

            position_i = self.calculateLocation(classification, buckets[i])
            estimated_locations[real_classification] = position_i

        ''' Estimate for the ones we were unable to locate '''
        for key, item in estimated_locations.iteritems():
            if item is not None:
                continue
            if not self.previous_locations[key].full():
                estimated_locations[key] = None
                continue

            ''' Get the ArrayQueue(previous locations) for robot with the 'key' identifier '''
            points_queue = self.previous_locations[key]
            trajectory_vector = linear_regression(points_queue)
            speed = self.getSpeed(key)


    ''' Measures speed in distance/frame '''
    def getSpeed(self, key):

        points_queue = self.previous_locations[key]
        if not points_queue.full():
            return None

        beginning_p = points_queue.getRight()
        end_p = points_queue.getLeft()

        size = points_queue.getMaxSize()
        speed = distance(beginning_p, end_p) ** (0.5) / size

        return speed


    def getRobotParameters(self, frame):

        all_contours = self.getMultiColorContours(frame, self.all_colors)
        buckets, bucket_counter = self.groupContours(all_contours)
        print "Bucket counter: ", bucket_counter
        print "Buckets: "
        for i in range(4):
            print "Bucket ----> ", i
            print buckets[i]
        # for bucket in buckets:
        #     print bucket

        bucket_classifications = self.classifyBuckets(buckets)

        print "Classifications: ", bucket_classifications



    # def getAllRobots(self, frame):

    #     helper_contours = {}
    #     helper_contours['pink'] = self.getContours(frame, 'pink', adjustments)
    #     helper_contours['green'] = self.getContours(frame, 'green',
    #                                                 adjustments)

    #     robots = {}
    #     for side_color in self.side_identifiers:
    #         side_contours = self.getContours(frame, side_color, adjustments)
    #         side_robots = self.getRobotCoordinates(side_contours,
    #                                                helper_contours['pink'])
    #         if (side_color == self.ally_color):
    #             robots['ally'] = side_robots
    #         else:
    #             robots['enemy'] = side_robots

    #     for side, side_robs in robots.iteritems():
    #         for color, robot in side_robs.iteritems():
    #             center = robot['center']
    #             orientation = self.getRobotOrientation(center, helper_contours,
    #                                                    color)
    #             robots[side][color]['orientation'] = orientation
    #             if center:
    #                 robots[side][color]['center'] = transformCoordstoDecartes(center)

    #     return robots

    # def getRobotCoordinates(self, side_contours, pink_contours):

    #     side_robots = {'green': {"orientation": None,
    #                              "center": None},
    #                    'pink': {"orientation": None,
    #                             "center": None}}
    #     for contour in side_contours:

    #         contour_center = self.getContourCenter(contour)
    #         pink_contour_count = 0

    #         for pink_contour in pink_contours:
    #             pink_contour_center = self.getContourCenter(pink_contour)

    #             dist = distance(pink_contour_center, contour_center)

    #             if dist < 20 * 20:
    #                 pink_contour_count += 1

    #         if pink_contour_count == 1:
    #             side_robots['green'] = {
    #                 "center": contour_center,
    #                 "orientation": None
    #             }
    #         elif pink_contour_count == 3:
    #             side_robots['pink'] = {
    #                 "center": contour_center,
    #                 "orientation": None
    #             }

    #     return side_robots

    # def getRobotOrientation(self, center, helper_contours, group_color):

    #     magnitude = 30.0

    #     # print(helper_contours)

    #     if center is None:
    #         return None, None

    #     if group_color == 'pink':
    #         main_color = 'pink'
    #         support_color = 'green'
    #     else:
    #         main_color = 'green'
    #         support_color = 'pink'

    #     # for _, cont in helper_contours:
    #     #     if cont == []:
    #     #         return None, None
    #     orientation_support = self.getKClosestContours(
    #         1, center, helper_contours[support_color])
    #     support_center = self.getContourCenter(orientation_support[0])

    #     orientation_main = self.getKClosestContours(
    #         3, center, helper_contours[main_color])
    #     orientation_main = self.getKFurthestContours(2, support_center,
    #                                                  orientation_main)

    #     if len(orientation_main) != 2:
    #         return None, None

    #     main_centers = self.getContourCenters(orientation_main)
    #     # print(main_centers)
    #     mean_main_point = meanPoint(main_centers)

    #     center = transformCoordstoDecartes(center)
    #     mean_main_point = transformCoordstoDecartes(mean_main_point)

    #     direction_vector = getDirectionVector(center, mean_main_point,
    #                                           magnitude)
    #     angle_radians = np.arctan2(direction_vector[1], direction_vector[0])
    #     angle_degrees = math.degrees(angle_radians)

    #     return (angle_degrees, direction_vector)
