#!/usr/bin/env python

import sys
from cv2 import imwrite


from numpy import mean, binary_repr, ones
from numpy.random import randint
from scipy.ndimage import zoom

for i in range(0, 16):
    img = ones((6, 6))*255
    img[1, 1] = 0
    img[4, 1] = 0
    img[1, 4] = 0

    if i%2 == 1:
        img[2, 2] = 0

    if (i>>1)%2 == 1:
        img[2, 3] = 0

    if (i>>2)%2 == 1:
        img[3, 2] = 0

    if (i>>3)%2 == 1:
        img[3, 3] = 0

    print (img)
    marker = zoom(img, zoom=50, order=0)

    imwrite('marker_images/marker_{}.png'.format(i), marker)
