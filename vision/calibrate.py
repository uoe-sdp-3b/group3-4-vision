#!/usr/bin/env python2.7
import cv2
import util
import numpy as np

class Calibrate():
    def __init__(self):
        pass

    def step(self):
        functions = [
            self.warp,
            self.undistort
            ]
        frame = cv2.imread("samples/pitch0/10_6x4.png")

        return util.compose(*functions)(frame)


    def process(self, frame):
        pass


    def pitch_to_numpy(self, pitch):
        ret = {}

        for key, value in pitch.iteritems():
            ret[key] = np.asarray(value)

        return ret

    def undistort(self, frame):
        pitches = util.read_json("config/undistort.json")

        pitch = self.pitch_to_numpy(pitches["0"])

        return cv2.undistort(frame, pitch["camera_matrix"], pitch["dist"], None,
                            pitch["new_camera_matrix"])

    def warp(self, frame):
        M = cv2.getRotationMatrix2D((640/2, 480/2), 3, 1)
        return cv2.warpAffine(frame, M, (640, 480))


    def fun(self):
        cv2.imshow("distort", self.step())
        cv2.waitKey(0)
