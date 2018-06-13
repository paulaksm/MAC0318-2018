import sys
import cv2
import time
import numpy as np
import os
from cmarkers import getCMarkers

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