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
import improved_GUI

class MainUiClass(QtGui.QMainWindow, improved_GUI.Ui_MainWindow,QtCore.QThread):
	def __init__(self, parent = None):
		super(MainUiClass, self).__init__(parent)
		self.setupUi(self)
		self.connect(self, QtCore.SIGNAL('main_img'), self.image_update)

		#publishes changes in settings
		self.GUI_settings_pub = rospy.Publisher("/drone_GUI_settings", String, queue_size=10)

		#connecting to the /drone_image topic to get images from camera
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/sfm_image", Image, self.callback)

		#reads default settings from main algorithm
		self.settings = image_converter().GUI_settings

		#linking buttons and their functions
		self.reset_btn.clicked.connect(self.reset_drone)
		self.land_btn.clicked.connect(self.land_drone)
		self.takeoff_btn.clicked.connect(self.takeoff_drone)
		self.x_speed_sl.valueChanged.connect(self.x_speed_val)
		self.y_speed_sl.valueChanged.connect(self.y_speed_val)
		self.up_h.valueChanged.connect(self.up_h_val)
		self.up_s.valueChanged.connect(self.up_s_val)
		self.up_v.valueChanged.connect(self.up_v_val)
		self.low_h.valueChanged.connect(self.low_h_val)
		self.low_s.valueChanged.connect(self.low_s_val)
		self.low_v.valueChanged.connect(self.low_v_val)
		self.show_mask.toggled.connect(self.apply_mask)

		#prevents arrow keys from focusing GUI elements
		self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)
	
	def setChildrenFocusPolicy(self, policy):
		def recursiveSetChildFocusPolicy(parentQWidget):
			for childQWidget in parentQWidget.findChildren(QtGui.QWidget):
				childQWidget.setFocusPolicy(policy)
				recursiveSetChildFocusPolicy(childQWidget)
		recursiveSetChildFocusPolicy(self)

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

		'''Direct control processing'''

	def keyPressEvent(self, eventQkeyEvent):
		key = eventQkeyEvent.key()
		speed = 1.5
		if key == QtCore.Qt.Key_W:
			self.settings['x_speed' ] = speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_S:
			self.settings['x_speed' ] = -speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_D:
			self.settings['y_speed' ] = -speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_A:
			self.settings['y_speed' ] = speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_Up:
			self.settings['z_speed' ] = speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_Down:
			self.settings['z_speed' ] = -speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_E:
			self.settings['yaw_speed' ] = -speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_Q:
			self.settings['yaw_speed' ] = speed
			self.GUI_settings_pub.publish(str(self.settings))

	def keyReleaseEvent(self, eventQkeyEvent):
		key = eventQkeyEvent.key()
		speed = 0
		if key == QtCore.Qt.Key_W:
			self.settings['x_speed' ] = speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_S:
			self.settings['x_speed' ] = -speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_D:
			self.settings['y_speed' ] = speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_A:
			self.settings['y_speed' ] = -speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_Up:
			self.settings['z_speed' ] = speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_Down:
			self.settings['z_speed' ] = -speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_E:
			self.settings['yaw_speed' ] = speed
			self.GUI_settings_pub.publish(str(self.settings))
		if key == QtCore.Qt.Key_Q:
			self.settings['yaw_speed' ] = -speed
			self.GUI_settings_pub.publish(str(self.settings))

	def reset_drone(self):
		print 'Reset'
		self.twist_pub = rospy.Publisher("/ardrone/reset", Empty, queue_size=10, latch = True)
		self.twist_pub.publish()

	def takeoff_drone(self):
		print 'See you later, nerds!'
		self.twist_pub2 = rospy.Publisher("/ardrone/takeoff", Empty, queue_size=10, latch = True)
		self.twist_pub2.publish()
		self.GUI_settings_pub.publish(str(self.settings))

	def land_drone(self):
		print 'Landing...'
		self.twist_pub2 = rospy.Publisher("/ardrone/land", Empty, queue_size=10, latch = True)
		self.twist_pub2.publish()
		self.GUI_settings_pub.publish(str(self.settings))

	def x_speed_val(self):
		x = self.x_speed_sl.value()
		self.settings['x_speed'] = x
		self.GUI_settings_pub.publish(str(self.settings))

	def y_speed_val(self):
		y = self.y_speed_sl.value()
		self.settings['y_speed'] = y
		self.GUI_settings_pub.publish(str(self.settings))


		'''Image mask settings'''


	def up_h_val(self):
		h = self.up_h.value()
		self.settings['upper_threshold'][0] = h
		print h
		self.GUI_settings_pub.publish(str(self.settings))
		self.up_h_label.setText("Hue: " + str(self.up_h.value()))

	def up_s_val(self):
		s = self.up_s.value()
		print s
		self.settings['upper_threshold'][1] = s
		self.GUI_settings_pub.publish(str(self.settings))
		self.up_s_label.setText("Saturation: " + str(self.up_s.value()))

	def up_v_val(self):
		v = self.up_v.value()
		self.settings['upper_threshold'][2] = v
		self.GUI_settings_pub.publish(str(self.settings))
		self.up_v_label.setText("Value: " + str(self.up_v.value()))

	def low_h_val(self):
		h = self.low_h.value()
		self.settings['lower_threshold'][0] = h
		print h
		self.GUI_settings_pub.publish(str(self.settings))
		self.low_h_label.setText("Hue: " + str(self.low_h.value()))

	def low_s_val(self):
		s = self.low_s.value()
		print s
		self.settings['lower_threshold'][1] = s
		self.GUI_settings_pub.publish(str(self.settings))
		self.low_s_label.setText("Saturation: " + str(self.low_s.value()))

	def low_v_val(self):
		v = self.low_v.value()
		self.settings['lower_threshold'][2] = v
		self.GUI_settings_pub.publish(str(self.settings))
		self.low_v_label.setText("Value: " + str(self.low_v.value()))

	def apply_mask(self):
		if self.show_mask.isChecked():
			self.settings['mask_toggle'] = 0
		else:
			self.settings['mask_toggle'] = 1
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