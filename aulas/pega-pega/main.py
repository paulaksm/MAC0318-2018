#!/usr/bin/python
import argparse

import tag

import sys
import cv2
import time
import numpy as np
import os
from cmarkers import getCMarkers, get_transform_matrix_points

# open camera
def open_camera(cam_id = 1):
    cap = cv2.VideoCapture(cam_id)
    return cap
 
# get frame
def get_frame(device):
    ret, img = device.read()
    if (ret == False): # failed to capture
        print >> sys.stderr, "Error capturing from video device."
        return None
    return img
 
# close camera
def cleanup(cam_id = 0): 
    cv2.destroyAllWindows()
    cv2.VideoCapture(cam_id).release()


# 4 points selected by the user in the corners of the board
corner_point_list = []
 
##
# This function is called by OpenCV when the user clicks
# anywhere in a window displaying an image.
##
def mouse_click_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # print ("Click at (%d,%d)" % (x,y))
        corner_point_list.append( (x,y) )

def find_centers(contours):
    centers = []
    for contour in contours:
        moments = cv2.moments(contour, True)
 
        center = (moments['m10']/moments['m00'] , moments['m01']/moments['m00'])
        # Convert floating point contour center into an integer so that
        # we can display it later.
        center = (int(round(center[0])),int(round(center[1])))
        centers.append(center)
    return centers

def find_contours(image):
    ret,thresh = cv2.threshold(image,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours

##
# Computes a perspective transform matrix by capturing a single
# frame from a video source and displaying it to the user for
# corner selection.
#
# Parameters:
# * dev: Video Device (from open_camera())
# * board_size: A tuple/list with 2 elements containing the width and height (respectively) of the gameboard (in arbitrary units, like inches)
# * dpi: Scaling factor for elements of board_size
# * calib_file: Optional. If specified, the perspective transform matrix is saved under this filename.
#   This file can be loaded later to bypass the calibration step (assuming nothing has moved).
##
def get_transform_matrix(dev, board_size, dpi, calib_file = None):
    # Read a frame from the video device
    img = get_frame(dev)
 
    # Displace image to user
    text = "[TOP_LEFT, BOTTOM_LEFT, TOP_RIGHT, BOTTOM_RIGHT]"
    cv2.putText(img, text, (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))
    cv2.imshow("Calibrate", img)
 
    # Register the mouse callback on this window. When 
    # the user clicks anywhere in the "Calibrate" window,
    # the function mouse_click_callback() is called (defined above)
    cv2.setMouseCallback("Calibrate", mouse_click_callback)
 
    # Wait until the user has selected 4 points
    while True:
        # If the user has selected all 4 points, exit loop.
        if (len(corner_point_list) >= 4):
            print ("Got 4 points: "+str(corner_point_list))
            break
 
        # If the user hits a key, exit loop, otherwise remain.
        if (cv2.waitKey(10) >= 0):
            break;
 
    # Close the calibration window:
    cv2.destroyWindow("Calibrate")
 
    # If the user selected 4 points
    if (len(corner_point_list) >= 4):
        # Do calibration
 
        # src is a list of 4 points on the original image selected by the user
        # in the order [TOP_LEFT, BOTTOM_LEFT, TOP_RIGHT, BOTTOM_RIGHT]
        src = np.array(corner_point_list, np.float32)
 
        # dest is a list of where these 4 points should be located on the
        # rectangular board (in the same order):
        a = [ (0, 0), (0, board_size[1]*dpi), (board_size[0]*dpi, 0), (board_size[0]*dpi, board_size[1]*dpi) ]
        dest = np.array(a, np.float32)
        print(corner_point_list)
        # Calculate the perspective transform matrix
        trans = cv2.getPerspectiveTransform(src, dest)
 
        # If we were given a calibration filename, save this matrix to a file
        if calib_file:
            np.savetxt(calib_file, trans)
        return trans
    else:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cam_id = 1
    dev = None

    parser.add_argument('-n',
                        '--nocamera',
                        action='store_false',
                        help='Disable camera, players need to send the position (default=False)')

    args = parser.parse_args()
    camera = args.nocamera

    dev = None

    if camera:
        dev = open_camera(cam_id)
 
    # The size of the board in inches, measured between the two
    # robot boundaries:
    board_size = [185, 215]
    maplines = [
        [40, 40, 40, 80],
        [40, 80, 60, 80],
        [60, 80, 60, 40],
        [60, 40, 40, 40],

        [40+70, 40+30, 40+70, 80+30],
        [40+70, 80+30, 60+70, 80+30],
        [60+70, 80+30, 60+70, 40+30],
        [60+70, 40+30, 40+70, 40+30]
    ]
    point = []
    if camera:
        board_size = [board_size[1], board_size[0]]
 
    # Number of pixels to display per inch in the final transformed image. This
    # was selected somewhat arbitrarily (I chose 17 because it fit on my screen):
    dpi = 5

    # Size (in pixels) of the transformed image
    transform_size = (int(board_size[0]*dpi), int(board_size[1]*dpi))
 
    # Calculate the perspective transform matrix
    transform = None
    if camera:
        # transform = get_transform_matrix(dev, board_size, dpi)
        transform = get_transform_matrix_points([(340, 10), (78, 1066), (1502, 6), (1806, 1045)], board_size, dpi)

    server = tag.TagServer(10318, board_size, maplines)

    while True:
        img_orig = None
        if camera:
            # pega uma imagem da camera
            img_orig = get_frame(dev)
        else:
            # cria uma imagem preta
            img_orig = np.zeros([transform_size[0], transform_size[1], 3])
            time.sleep(0.1)

        start = time.time()
        if img_orig is not None: # if we did get an image
            img = img_orig
            if camera:
                img = cv2.warpPerspective(img_orig, transform, dsize=transform_size)
                e1 = cv2.getTickCount()
                # your code execution
                markers = getCMarkers(img)
                e2 = cv2.getTickCount()
                tt = (e2 - e1)/ cv2.getTickFrequency()
                # print("mk", tt)

                for i in markers:
                    idd, p, head = i
                    server.updatePosition(idd, p[0]/dpi, p[1]/dpi, head)
                    p = (int(p[0]), int(p[1]))
                    cv2.circle(img, p, 30, (0,255,0))
                    cv2.putText(img, str(idd), p, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255))

            for line in maplines:
                color = (255, 255, 255)
                line = np.array(line)*dpi
                cv2.line(img, (line[0], line[1]), (line[2], line[3]), color)
            for robot in server.robots():
                for line in robot.lines():
                    p1 = (line[0]*dpi).astype(int)
                    p2 = (line[1]*dpi).astype(int)
                    color = (255, 255, 0)
                    if robot == server.tag:
                        color = (0, 0, 255)
                    cv2.line(img, (p1[0], p1[1]), (p2[0], p2[1]), color)

            if server.paused:
                cv2.putText(img, "PAUSE", (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))
            # res = cv2.resize(img,None,fx=.5, fy=.5)
            end = time.time()
            seconds = end - start
            fps  = 1.0 / seconds
            start = time.time()
            if camera:
                cv2.putText(img, str(fps), (0,60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))
            res = img
            cv2.imshow("warped", res)
 
        else: # if we failed to capture (camera disconnected?), then quit
            break
 
        k = cv2.waitKey(1)
        if k == 115: # s
            server.startGame()
        elif k == 112: # p
            server.stopGame()
        elif k == 113: # q
            server.stop()
            break

    if camera:
        cleanup(cam_id)
