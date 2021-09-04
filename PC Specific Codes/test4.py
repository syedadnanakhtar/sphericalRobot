#find good points to track, calculate optical flow, print the weighted average. if the average is above a certain threshold, then dont show the image frame.

#!/usr/bin/env python

'''
Lucas-Kanade tracker
====================

Lucas-Kanade sparse optical flow demo. Uses goodFeaturesToTrack
for track initialization and back-tracking for match verification
between frames.

Usage
-----
lk_track.py [<video_source>]


Keys
----
ESC - exit
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2
import math
import video
from common import anorm2, draw_str
from time import clock

def run():
    lk_params = dict( winSize  = (15, 15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    feature_params = dict( maxCorners = 10,
                           qualityLevel = 0.5,
                           minDistance = 7,
                           blockSize = 20  )
    feature_detect_interval = 5
    motion_threshold = 40
    stable_video_flag = True

    frame_id = 0

    #Determine the source of video
    cap = cv2.VideoCapture('C:\Users\NCETIS\Documents\MATLAB\Media3_cropped2.avi')
    read_flag, im_color = cap.read()
    im_initial = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)
    vis =im_color.copy()  # frame copied to vis

    while True:
        #Capture one frame from video
        read_flag, im_color = cap.read()
        vis = im_color.copy()  # frame copied to vis
        if (read_flag == False):
            break

        #convert colored frame to black and white
        im_final = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)

        #detect good features to track every 5 frames
        if (frame_id % feature_detect_interval == 0):
            p0 = cv2.goodFeaturesToTrack(im_initial, mask=None, **feature_params)
            n_features = p0.shape[0]

        #calculate optical flow at those points
        p1, st, err = cv2.calcOpticalFlowPyrLK(im_initial, im_final, p0, None, **lk_params) #opt_flow is numpy.ndarray
        n_flow_vectors = p1.shape[0]
        opt_flow = p1-p0
        p0=p1
        #print (opt_flow.shape)


        #Assert the shape of optical flow and feature points
        assert (n_features == n_flow_vectors), "number of flow vectors is not equal to number of feature points"

        #Find the average of the vectors
        x_sum = np.sum(opt_flow,axis=0)[0][0]
        y_sum = np.sum(opt_flow,axis=0)[0][1]
        x_avg = x_sum / n_flow_vectors
        y_avg = y_sum / n_flow_vectors
        norm = math.sqrt( x_avg**2 + y_avg**2 )


        #draw arrowed line and add text
        cv2.arrowedLine(vis, (639, 356), (639 + int(x_avg), 356 + int(y_avg)), color=0, thickness=2)
        draw_str(vis, (20, 20), 'Euclidean Norm: %d' % norm)

        #play the video
        if ( not stable_video_flag or norm <= motion_threshold):
            cv2.imshow('Video', vis)

        #check if escape key is pressed
        ch = cv2.waitKey(20)
        if ch == 27:
            break

        #make im_final equal im_initial
        im_initial = im_final
        frame_id = frame_id + 1

    cv2.destroyAllWindows()
    cap.release()

#def draw_flow(img, flow, step=16):



run()