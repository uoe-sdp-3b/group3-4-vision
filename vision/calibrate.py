#!/usr/bin/env python2.7
import sys
sys.path.insert(0, '../')
sys.path.insert(0, './')
import cv2
import util
import numpy as np
from functools import partial

COLS = 640
ROWS = 480


def step(frame, pitch):
    functions = [
        perspective,
        #translate,
        partial(undistort, pitch),
        #warp,
        translate,
        warp,
        ]

    return util.compose(*functions)(frame)


def pitch_to_numpy(pitch):
    ret = {}

    for key, value in pitch.iteritems():
        ret[key] = np.asarray(value)

    return ret


def translate(frame):
    M = np.float32([[1, 0, -5], [0, 1, -8]])
    return cv2.warpAffine(frame, M, (640, 480))


def undistort(pitches, frame):

    pitch = pitch_to_numpy(pitches)

    return cv2.undistort(frame, pitch["camera_matrix"], pitch["dist"], None,
                         pitch["new_camera_matrix"])


def warp(frame):
    M = cv2.getRotationMatrix2D((COLS/2, ROWS/2), 1, 1)
    return cv2.warpAffine(frame, M, (COLS, ROWS))


def perspective(frame):
    pts1 = np.float32([[48,33],[38,456],[595,468],[597,29]])
    pts2 = np.float32([[4,5],[5,475],[632,476],[636,6]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    dst = cv2.warpPerspective(frame, M, (640, 480))

    return dst
