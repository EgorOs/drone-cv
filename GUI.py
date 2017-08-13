from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.resetBtn = QtGui.QPushButton(self.centralwidget)
        self.resetBtn.setGeometry(QtCore.QRect(690, 270, 98, 27))
        self.resetBtn.setStyleSheet(_fromUtf8("font: 11pt \"NanumBarunGothic\";"))
        self.resetBtn.setObjectName(_fromUtf8("resetBtn"))
        self.camera_img = QtGui.QLabel(self.centralwidget)
        self.camera_img.setGeometry(QtCore.QRect(60, 40, 401, 271))
        self.camera_img.setStyleSheet(_fromUtf8("border:1px solid rgb(12, 12, 12);"))
        self.camera_img.setText(_fromUtf8(""))
        self.camera_img.setObjectName(_fromUtf8("camera_img"))
        self.X_Slider = QtGui.QSlider(self.centralwidget)
        self.X_Slider.setGeometry(QtCore.QRect(660, 80, 160, 29))
        self.X_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.X_Slider.setObjectName(_fromUtf8("X_Slider"))
        #modified slider
        self.X_Slider.setMinimum(0)
        self.X_Slider.setMaximum(180)
        self.X_Slider.setTickInterval(1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(710, 50, 66, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.Y_Slider_2 = QtGui.QSlider(self.centralwidget)
        self.Y_Slider_2.setGeometry(QtCore.QRect(660, 130, 160, 29))
        self.Y_Slider_2.setOrientation(QtCore.Qt.Horizontal)
        self.Y_Slider_2.setObjectName(_fromUtf8("Y_Slider_2"))
        #modified slider
        self.Y_Slider_2.setMinimum(0)
        self.Y_Slider_2.setMaximum(180)
        self.Y_Slider_2.setTickInterval(1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(710, 110, 66, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.resetBtn_2 = QtGui.QPushButton(self.centralwidget)
        self.resetBtn_2.setGeometry(QtCore.QRect(690, 190, 98, 27))
        self.resetBtn_2.setStyleSheet(_fromUtf8("font: 11pt \"NanumBarunGothic\";"))
        self.resetBtn_2.setObjectName(_fromUtf8("resetBtn_2"))
        self.resetBtn_3 = QtGui.QPushButton(self.centralwidget)
        self.resetBtn_3.setGeometry(QtCore.QRect(690, 230, 98, 27))
        self.resetBtn_3.setStyleSheet(_fromUtf8("font: 11pt \"NanumBarunGothic\";"))
        self.resetBtn_3.setObjectName(_fromUtf8("resetBtn_"))
        self.resetBtn_4 = QtGui.QPushButton(self.centralwidget)
        self.resetBtn_4.setGeometry(QtCore.QRect(690, 310, 98, 27))
        self.resetBtn_4.setStyleSheet(_fromUtf8("font: 11pt \"NanumBarunGothic\";"))
        self.resetBtn_4.setObjectName(_fromUtf8("resetBtn_4"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.resetBtn.setText(_translate("MainWindow", "Reset", None))
        self.label.setText(_translate("MainWindow", "X speed", None))
        self.label_2.setText(_translate("MainWindow", "Y speed", None))
        self.resetBtn_2.setText(_translate("MainWindow", "Stop", None))
        self.resetBtn_3.setText(_translate("MainWindow", "Land", None))
        self.resetBtn_4.setText(_translate("MainWindow", "Take off", None))
