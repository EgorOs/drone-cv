#!/usr/bin/env python

#tutorial https://www.youtube.com/watch?v=ivcxZSHL7jM
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from val import randValue
import time

#import pre-designed ui "pyuic4 'filename.ui'"
import GUI

class MainUiClass(QtGui.QMainWindow, GUI.Ui_MainWindow):
	def __init__(self, parent = None):
		super(MainUiClass, self).__init__(parent)
		self.setupUi(self)
		self.threadclass = ThreadClass()
		self.threadclass.start()
		self.connect(self.threadclass, QtCore.SIGNAL('VAL'), self.updateProgressBar)

	def updateProgressBar(self,val):
		self.progressBar.setValue(val)

class ThreadClass(QtCore.QThread):
	def __init__(self, parent = None):
		super(ThreadClass, self).__init__(parent)	

	def run(self):
		while  1:
			val = randValue()
			print val 	 	
			time.sleep(0.5)
			self.emit(QtCore.SIGNAL('VAL'), val)
if __name__ == '__main__':
	a = QtGui.QApplication(sys.argv)
	app = MainUiClass()
	app.show()
	a.exec_()