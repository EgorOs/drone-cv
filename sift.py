#!/usr/bin/env python
import cv2
import numpy as np
def process_image(imagename, params = "--edge-thresh 10 --peak-thresh 5"):
    r,g,b = cv2.split(imagename)
    grayscale = 0.2989*r + 0.5870*g + 0.1140*b
    cv2.imwrite('temp.pgm', grayscale[cv2.cv.CV_IMWRITE_PXM_BINARY, 1])
    #f = np.loadtxt('temp.pgm')
    #print(f)
    pass