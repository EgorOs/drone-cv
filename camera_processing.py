#!/usr/bin/env python
from __future__ import print_function
#importing standart modules
import roslib
import sys
import rospy
import cv2
import cv2.cv as cv
import numpy as np
from scipy import signal
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

def getTargetPosition(self, lower_threshold, upper_threshold):

	#getting image parameters
	(rows,cols,channels) = self.shape
	
	#denoise image
	self = cv2.medianBlur(self,5)

	#COLOR DETECTION

	#change color space to "hue/saturation/value"
	hsv = cv2.cvtColor(self, cv2.COLOR_BGR2HSV)

	#create mask and apply it, only not masked of image are visible
	mask = cv2.inRange(hsv, lower_threshold, upper_threshold)

	#create black single-channel 8-bit background, no need to convert to grayscale later
	background = np.zeros((rows,cols,1), np.uint8)
	res = cv2.bitwise_not(background, background, mask = mask)
	#res = cv2.bitwise_and(self, self, mask = mask) #for colored mask

	#SHAPE DETECTION
	try:
		circles = cv2.HoughCircles(res, cv.CV_HOUGH_GRADIENT, 2, 600, param1=50,param2=30,minRadius=0,maxRadius=250)
		circles = np.uint16(np.around(circles))				#array of [x,y,radius]
	except:
		#cv2.imshow("image window", self)
		#cv2.imshow("masked image", res)
		cv2.waitKey(3)
	return circles, res

def frameDifference(self, prev):
	(rows,cols,channels) = self.shape
	background = np.zeros((rows,cols,1), np.uint8)
	try:
		diff = self - prev
		m = diff != 0
		m = (m + [0])*255
		#diff = curr_frame - prev_frame
		cv2.imshow("image window", diff - 100)
	except:
		print("no prev_frame yet")
	prev = self
	#prev_frame = curr_frame.copy()
	return diff, prev

def depthMap(self):

	#masks
	L3 = np.matrix([[1,2,1]])	#local averaging
	E3 = np.matrix([[-1,0,1]])	#edge detection
	S3 = np.matrix([[-1,2,-1]])	#spot detection

	#masks 3x3
	L3tL3 = L3.transpose()*L3
	L3tE3 = L3.transpose()*E3
	L3tS3 = L3.transpose()*S3
	E3tL3 = E3.transpose()*L3
	E3tE3 = E3.transpose()*E3
	E3tS3 = E3.transpose()*S3
	S3tL3 = S3.transpose()*L3
	S3tE3 = S3.transpose()*E3
	S3tS3 = S3.transpose()*S3

	YCrCb = cv2.cvtColor(self, cv2.COLOR_BGR2YCR_CB)
	Y,Cr,Cb = cv2.split(YCrCb)

	#scipt.signal.convolve2d might work
	dst = cv2.filter2D(Y, -1, L3tL3)
	sy = signal.convolve2d(Y,L3tL3, mode='same')
	#sr = signal.convolve2d(Cr,S3tS3, mode='same')
	#sg = signal.convolve2d(Cb,S3tS3, mode='same')
	#print(sy)
	cv2.imshow("Y channel", Y)
	cv2.imshow("Cr channel", Cr)
	cv2.imshow("Cb channel", Cb)
	cv2.imshow("DST", dst)

	pass

def surfTest(self, param):


	gray = cv2.cvtColor(self,cv2.COLOR_BGR2GRAY)
	surf = cv2.SURF(param)
	kp, des = surf.detectAndCompute(self,None)

	img = cv2.drawKeypoints(gray, kp, self, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("SURF", img)
	pass