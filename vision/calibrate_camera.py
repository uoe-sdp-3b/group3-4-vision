import numpy as np
import cv2
import glob
import json
from copy import copy

class Configure():
    def __init__(self):
        self.objpoints = []
        self.imgpoints = []
        #self.camera = cv2.VideoCapture(0)
        self.height = 480
        self.width = 640

    def getCalibrationParameters(self):
        dim = (7,5)
        objp = np.zeros((dim[0]*dim[1], 3), np.float32)
        objp[:,:2] = np.mgrid[0:dim[0], 0:dim[1]].T.reshape(-1,2)
        images = glob.glob('samples/pitch0/*.png')
        #print "images: %s" % images
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (7,5), None)
            #cv2.imshow('chess_board_corners', corners)
            #cv2.waitkey(5)
            # If found, add object points, image points (after refining them)
            if ret == True:
                self.objpoints.append(objp)
                corners2 = copy(corners)
                #_ = cv2.cornerSubPix(gray,corners2,(11,11),(-1,-1),criteria)
                self.imgpoints.append(corners2)

                # Draw and display the corners
                # Comment this out to skip showing sample images!
                _ = cv2.drawChessboardCorners(img, dim, corners2, ret)
                cv2.imshow('img',img)
       	    cv2.waitKey(1000)

        ret, camera_matrix, dist, _, _ = cv2.calibrateCamera(self.objpoints, self.imgpoints, gray.shape[::-1],None,None)
        new_camera_matrix, roi=cv2.getOptimalNewCameraMatrix(camera_matrix, dist,(self.width,self.height),0,(self.width,self.height))

        pitch1 = {'new_camera_matrix' : new_camera_matrix,
            'roi' : roi,
            'camera_matrix' : camera_matrix,
            'dist' : dist}

        pitch0 = {'new_camera_matrix' : new_camera_matrix,
            'roi' : roi,
            'camera_matrix' : camera_matrix,
            'dist' : dist}

        data = {0 : pitch0, 1: pitch1}
        
        with open('undistort.json', 'w') as f:
            f.write(json.dumps(data))

C = Configure()
C.getCalibrationParameters()
            
