#!/usr/bin/env python
from __future__ import print_function
#importing standart modules
import roslib
import sys
import rospy
import cv2
import cv2.cv as cv
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

#default_height = 100;
Kp = 0.005;
Ki = 0.0001;
Kd = 0.01;

#1st argument is image from camera, 2nd is data about position of target (circle)
def getCoordData(image, target):

	#getting image shape
	(rows,cols,channels) = image.shape

	#linking origin of coordinates to the center of image
	position = (target - [cols/2, rows/2, 0])*[1,-1,1]
	
	#getting x, y and raduis of target
	x, y, r = position[0,0,0], position[0,0,1], position[0,0,2]

	#enable|disable debug features
	DEBUG = False
	if DEBUG is True:
		sys.stdout.write("\r{0}>".format("x= "+ str(x) + ' ; ' +"y= "+ str(y) + ' ; ' +"r= "+ str(r)))
		sys.stdout.flush()
	
	#output
	return x, y, r

def coordRegulator(x,y,r):
	if abs(x)>1.2*r:
		sign_x = x/abs(x)
		x_out = sign_x*Kp*abs(x) # + Kd*(x-old_x)/(current_time-previous_time) + Ki*x*(current_time-previous_time)
		old_x = x;
		if abs(x_out)>1:
			x_out = sign_x;
	else:
		x_out = 0

	if abs(y)>1.2*r:
		sign_y = y/abs(y)
		y_out = sign_y*Kp*abs(y) # + Kd*(y-old_y)/(current_time-previous_time) + Ki*y*(current_time-previous_time)
		y_old = y
		if abs(y_out)>1:
			y_out = sign_y;
	else:
		y_out = 0

	#enable|disable debug features
	DEBUG = False
	if DEBUG is True:
		sys.stdout.write("\r{0}>".format("x= "+ str(x_out) + ' ; ' +"y= "+ str(y_out)))	
		sys.stdout.flush()

	#output
	return x_out, y_out