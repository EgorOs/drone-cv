#!/usr/bin/env python

#tutorial https://www.youtube.com/watch?v=ivcxZSHL7jM
import roslib
import sys
import rospy
import cv2
import cv2.cv as cv
import numpy as np
from std_msgs.msg import String, Empty
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4 import QtCore
from val import randValue
import time

from cv_control import image_converter
#temp, being used to create Twist messages
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
#/temp

#import pre-designed ui "pyuic4 'filename.ui'"
import GUI

class MainUiClass(QtGui.QMainWindow, GUI.Ui_MainWindow,QtCore.QThread):
	def __init__(self, parent = None):
		super(MainUiClass, self).__init__(parent)
		self.setupUi(self)
		self.connect(self, QtCore.SIGNAL('main_img'), self.image_update)

		#publishes changes in settings
		self.GUI_settings_pub = rospy.Publisher("/drone_GUI_settings", String, queue_size=10)

		#connecting to the /drone_image topic to get images from camera
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/drone_image", Image, self.callback)

		#reads default settings from main algorithm
		self.settings = image_converter().GUI_settings

		#linking buttons and their functions
		self.resetBtn.clicked.connect(self.reset_drone)
		self.resetBtn_3.clicked.connect(self.land_drone)
		self.resetBtn_4.clicked.connect(self.takeoff_drone)
		self.X_Slider.valueChanged.connect(self.x_sl_val)
		self.Y_Slider_2.valueChanged.connect(self.y_sl_val)


		'''Image window processing'''


	def callback(self, data):

		#gets image from /drone_image and passes it to 'main_ing' thread
		cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		self.emit(QtCore.SIGNAL('main_img'), cv_image)

	def image_update(self,val):

		#convert cv bgr image to QT rgb format
		b,g,r = cv2.split(val)
		rgb_img = cv2.merge([r,g,b])
		height, width, channel = rgb_img.shape
		bytesPerLine = 3 * width
		qImg = QImage(rgb_img.data, width, height, bytesPerLine, QImage.Format_RGB888)

		#updates image in main window
		self.camera_img.setGeometry(QtCore.QRect(20, 20, width, height))
		self.camera_img.setPixmap(QtGui.QPixmap(qImg)) #to resize image after (qImg) add .scaledToWidth(90)		


		'''Buttons processing'''


	def reset_drone(self):
		print 'Reset'
		#self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
		#self.twist_pub.publish(Twist(Vector3(1,1,0), Vector3(0,0,1)))
		self.twist_pub = rospy.Publisher("/ardrone/reset", Empty, queue_size=10)
		self.twist_pub.publish()


	def takeoff_drone(self):
		print 'See you later, nerds!'
		self.twist_pub2 = rospy.Publisher("/ardrone/takeoff", Empty, queue_size=10)
		self.twist_pub2.publish()
		self.settings['mask_toggle'] = 0
		self.GUI_settings_pub.publish(str(self.settings))

	def land_drone(self):
		print 'Landing...'
		self.twist_pub2 = rospy.Publisher("/ardrone/land", Empty, queue_size=10)
		self.twist_pub2.publish()
		#self.settings['lower_threshold'] = [80,50,50]
		self.settings['mask_toggle'] = 1
		self.GUI_settings_pub.publish(str(self.settings))

	def x_sl_val(self):
		h = self.X_Slider.value()
		self.settings['lower_threshold'] = [h,50,50]
		print h
		self.GUI_settings_pub.publish(str(self.settings))

	def y_sl_val(self):
		h2 = self.Y_Slider_2.value()
		self.settings['upper_threshold'] = [h2,255,255]
		print h2
		self.GUI_settings_pub.publish(str(self.settings))

class ImageThread(QtCore.QThread):
	def __init__(self, parent = None):
		super(ImageThread, self).__init__(parent)	

if __name__ == '__main__':
	rospy.init_node('Drone_GUI_Image', anonymous = True)
	a = QtGui.QApplication(sys.argv)
	app = MainUiClass()
	app.show()
	a.exec_()