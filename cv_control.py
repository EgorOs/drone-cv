#!/usr/bin/env python
from __future__ import print_function
#importing standart modules
import roslib
import sys
import rospy
import cv2
import cv2.cv as cv
import numpy as np
import yaml #allows to convert string to dict
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
#importing custom modules
from coordinates_processing import getCoordData, coordRegulator
from camera_processing import getTargetPosition#, frameDifference, depthMap, surfTest

class image_converter:
	#publishes on image_topic_2, type of message: Image
	def __init__(self):
		self.image_pub = rospy.Publisher("/drone_image", Image)
		#self.twist_pub = rospy.Publisher("/drone_velocity", Twist)
		self.twist_pub = rospy.Publisher("/cmd_vel", Twist)

		self.bridge = CvBridge()
		##self.image_sub = rospy.Subscriber("/ardrone/front/image_raw", Image, self.callback)
		#rosservice call /ardrone/togglecam - switching between cameras via console
		self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)

		#getting settings from GUI
		self.settings_sub = rospy.Subscriber("/drone_GUI_settings", String, self.getSettings)
		
		#declaring variables within a class
		#default settings
		self.GUI_settings = {
		'lower_threshold':[110,50,50],
		'upper_threshold':[130,255,255],
		'mask_toggle':1,
		'x_speed':0,
		'y_speed':0,
		'z_speed':0,
		'yaw_speed':0,
		'roll_speed':0,
		'pitch_speed':0,
		}

	def getSettings(self,data):

		#converting string into a dictionary, cutting 6 extra letters
		self.GUI_settings = eval(str(data).replace('data: ', ''))

	def callback(self, data):
		print(self.GUI_settings['upper_threshold'])
		print(self.GUI_settings['lower_threshold'])
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
			original_img = cv_image.copy()
		except CvBridgeError as e:
			print(e)

		#image parameters
		(rows,cols,channels) = cv_image.shape

		#flip image horizontally
		#cv_image = cv2.flip(cv_image, 1)

		#getting the position of target
		lower_threshold = np.array(self.GUI_settings['lower_threshold'])
		upper_threshold = np.array(self.GUI_settings['upper_threshold'])
		circles,res = getTargetPosition(cv_image, lower_threshold, upper_threshold)
		#try:
		#	frameDifference(cv_image,prev_frame)
		#except:
		#	print("no prev img")
		#global prev_frame
		#prev_frame = cv_image

		#depthMap(cv_image)
		#ct = surfTest(cv_image, 1100)

		#print(type(circles)) #it is possible to make a callback here in case if target was lost

		#coordinates processing
		if isinstance(circles, np.ndarray):			#check if circles is ndarray to prevent type errors, maybe we shall set the ndarray type earlier
			x,y,r = getCoordData(cv_image, circles)
			x_out,y_out = coordRegulator(x,y,r)

		#drawing on image
		if isinstance(circles, np.ndarray):			#check if circles is ndarray to prevent type errors, maybe we shall set the ndarray type earlier
			for i in circles[0,:]:
				cv2.circle(cv_image,(i[0],i[1]), i[2], (255,255,0),1)
				cv2.circle(cv_image,(i[0],i[1]),2,(0,0,255),3)
				cv2.line(cv_image,(cols/2,rows/2),(i[0],i[1]),(0,0,0),1)
			cv2.line(cv_image,(cols/2,0),(cols/2,rows),(0,0,0),1)
			cv2.line(cv_image,(0,rows/2),(cols,rows/2),(0,0,0),1)
			#cv2.imshow("image window", cv_image)
			#cv2.imshow("masked image", res)
			cv2.waitKey(3)

		try:
			if self.GUI_settings['mask_toggle'] == 0:	
				masked_image = cv2.bitwise_and(original_img, original_img, mask = res)
			else:
				masked_image = cv_image
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(masked_image ,"bgr8"))
			self.twist_pub.publish(Twist(Vector3( \
			float(self.GUI_settings['x_speed'])/5, \
			float(self.GUI_settings['y_speed'])/5,\
			float(self.GUI_settings['z_speed'])/2,), Vector3(0,0,float(self.GUI_settings['yaw_speed'])/2)))
		except CvBridgeError as e:
			print(e)
def main(args):
	ic = image_converter()
	rospy.init_node("image_converter", anonymous = True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("shutting down")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)