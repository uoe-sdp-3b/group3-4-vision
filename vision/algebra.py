import math
import numpy as np
from vector import Vector
from array_queue import ArrayQueue

def distance(point_1, point_2):

    dx = ( point_1[0] - point_2[0] )
    dy = ( point_1[1] - point_2[1] )

    '''Not the mathematical distance, but
    root is an expensive op, and we don't really need it'''
    return dx * dx + dy * dy


def meanPoint(points):

    tx = 0.0
    ty = 0.0

    for point in points:
        tx += point[0]
        ty += point[1]

    l = len(points)
    if l == 0:
        return None

    return ( tx / l, ty / l )


def transformCoordstoDecartes( (x, y) ):
    return ( x - 320, 240 - y )

def transformCoordstoCV( (x, y) ) :
    return ( x + 320, 240 - y )

def linear_regression(points_queue):

    points = points_queue.iteritems()
    print "Points -----> ", points

    if None in points:
        return None # Might need revisiting 

    if distance(points[0], meanPoint(points)) < 10:
        return Vector(0, 0)

    num_pts = len(points)
    M = np.array([points[0]])
    for i in range(1, num_pts):
        print points[i]
        np.append(M, [points[i]], axis=0)

    xc = M[:, [0]]
    print "Xc --------->", xc
    yc = M[:, [1]]
    print "Yc --------->", yc
    ones = np.ones((num_pts, 1))
    X = np.concatenate((ones, xc), axis=1)

    X_intermediary = np.dot(X.T, X)
    Y_intermediary = np.dot(X.T, yc)

    R = np.dot(inv(X_intermediary), Y_intermediary)

    k = R[1][0]

    beginning_x = points_queue.getRight()[0]
    end_x = points_queue.getLeft()[0]

    if beginning_x < end_x:
        return Vector(1, k)
    else:
        return Vector(-1, -k)

