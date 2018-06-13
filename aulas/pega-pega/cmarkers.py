import cv2
import numpy as np
import math

def getCMarkers (img):
    e1 = cv2.getTickCount()
    markers = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10)
    
    ####print("threshold", (cv2.getTickCount() - e1)/ cv2.getTickFrequency())
    kernel = np.ones((2,2),np.uint8)
    img2 = cv2.morphologyEx(img3, cv2.MORPH_CLOSE, kernel)
    ####print("close", (cv2.getTickCount() - e1)/ cv2.getTickFrequency())
    # cv2.imshow("m3", img2)
    # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    # img2 = cv2.dilate(img2,kernel,iterations = 2)

    kernel = np.ones((2,2),np.uint8)
    img2 = cv2.dilate(img2,kernel, 1)

    # cv2.imshow("m3", img2)
    ####print("dilate", (cv2.getTickCount() - e1)/ cv2.getTickFrequency())
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
    params.filterByInertia = False
    params.filterByConvexity = False

    # # Change thresholds
    # params.minThreshold = 240
    # params.maxThreshold = 255
    # params.thresholdStep = 1

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 5
    params.minDistBetweenBlobs = 1

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.5

    # # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.70
        
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.2
    params.filterByColor = False

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)


    # Detect blobs.
    keypoints = detector.detect(img2)


    ####print("blob", (cv2.getTickCount() - e1)/ cv2.getTickFrequency())

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
    # the size of the circle corresponds to the size of blob
    k = []
    kk = []
    #####print(len(keypoints))
    for point  in keypoints:
        count = []
        for p  in keypoints:
            if p == point:
                continue
            elif (p.pt[0]-point.pt[0])**2+(p.pt[1]-point.pt[1])**2 <= (point.size*4.5)**2 and (abs(point.size/p.size-1) <= 0.3):
                count.append(p.pt)
        if len(count) >= 2:
            k.append((point.pt, count))
            kk.append(point)

    ####print("near", (cv2.getTickCount() - e1)/ cv2.getTickFrequency())
    for point in k:
        p, near = point
        # distance open the angre and 90 degree
        midistance = math.pi/30.0
        bottom = [] 
        rigth = [] 
        for p1 in near:
            for p2 in near:
                if p1 == p2:
                    continue
                u = np.array([p1[0]-p[0], p1[1]-p[1]])
                v = np.array([p2[0]-p[0], p2[1]-p[1]])
                angle = np.math.atan2(np.linalg.det([u,v]),np.dot(u,v))
                if abs(angle-math.pi/2.0) < math.pi/30.0:
                    bottom = p1
                    rigth = p2

                    
                    conner = rigth+u
                    addu = u/6.0
                    addv = v/6.0
                    conners = [p-addu-addv, bottom+addu-addv, rigth-addu+addv, conner+addu+addv]
                    trans = get_transform_matrix_points(conners, [10, 10], 10)
                    code = cv2.warpPerspective(gray, trans, dsize=(100, 100))
                    # code = cv2.adaptiveThreshold(code, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 1)

                    number = getNumber(code, 160)
                    if number == False:
                        continue
                    # cv2.imshow("m2", code)


                    uu = np.array([0, 1])
                    angle = np.math.atan2(np.linalg.det([v,uu]),np.dot(v,uu))

                    mid = p+u*0.5+v*0.5
                    if number != 0:
                        markers.append([number, mid, angle])
    
    img2 = cv2.drawKeypoints(img2, kk, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # cv2.imshow("m3", img2)
    return markers

def getNumber(img, threshold):
    vsplit = np.vsplit(img, 4)
    mean = []
    for vs in vsplit:
        m = []
        hsplit = np.hsplit(vs, 4)
        for hs in hsplit:
            m.append(np.mean(hs))
        mean.append(m)
    # print(np.array(mean).astype(np.uint8))
    # print((mean[0][0]+mean[3][3])/2.0)
    threshold = (mean[0][0]+mean[3][3])/2.0*0.85
    print(threshold)
    mean = np.array(mean) >= threshold
    valid = mean[0, 0] == False
    valid = valid and mean[0, 3] == False
    valid = valid and mean[0, 3] == False
    valid = valid and mean[1, 0] == True
    valid = valid and mean[0, 1] == True
    valid = valid and mean[2, 0] == True
    valid = valid and mean[0, 2] == True
    valid = valid and mean[3, 3] == True
    valid = valid and mean[1, 3] == True
    valid = valid and mean[3, 1] == True
    valid = valid and mean[2, 3] == True
    valid = valid and mean[3, 2] == True
    if valid == False:
        return False
    number  = 0
    if not mean[1, 1]:
        number += 1
    if not mean[1, 2]:
        number += 2
    if not mean[2, 1]:
        number += 4
    if not mean[2, 2]:
        number += 8
    return number

def get_transform_matrix_points(corners, board_size, dpi):
    # Read a frame from the video device

    # Close the calibration window:
    # cv2.destroyWindow("Calibrate")
 
    # If the user selected 4 points
    if (len(corners) == 4):
        # Do calibration
 
        # src is a list of 4 points on the original image selected by the user
        # in the order [TOP_LEFT, BOTTOM_LEFT, TOP_RIGHT, BOTTOM_RIGHT]
        src = np.array(corners, np.float32)
 
        # dest is a list of where these 4 points should be located on the
        # rectangular board (in the same order):
        dest = np.array( [ (0, 0), (0, board_size[1]*dpi), (board_size[0]*dpi, 0), (board_size[0]*dpi, board_size[1]*dpi) ], np.float32)
 
        # Calculate the perspective transform matrix
        trans = cv2.getPerspectiveTransform(src, dest)
 
        # If we were given a calibration filename, save this matrix to a file
        return trans
    else:
        return None
