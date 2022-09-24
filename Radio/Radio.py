# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Radio.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

######
def getchannel():
    return 76.7
def setvolume(a):
    print("setting volume ",a)
    
def seek(a):
    print("seeking",a)
def changechannel(a):
    
    print("changing channel", a)

class Ui_Radio(object):
    def seekN(self):
        a=float(float(getchannel())/float(10))
        self.label_2.setText(str(a))
        font = self.label_2.font()
        font.setPointSize(26)
        font.setBold(True)
        self.label_2.setFont(font)
        seek(1)
    def seekP(self):
        a=float(float(getchannel())/float(10))
        self.label_2.setText(str(a))
        font = self.label_2.font()
        font.setPointSize(26)
        font.setBold(True)
        self.label_2.setFont(font)
        seek(0)
    def BackHome(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_HomeMainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        
    def changechannel89(self):
        a=89.0
        self.label_2.setText(str(a))
        font = self.label_2.font()
        font.setPointSize(26)
        font.setBold(True)
        self.label_2.setFont(font)
        changechannel(890)
    
    def changechannel91(self):
        a=91.0
        self.label_2.setText(str(a))
        font = self.label_2.font()
        font.setPointSize(26)
        font.setBold(True)
        self.label_2.setFont(font)
        changechannel(910)
        
    def changechannel96(self):
        a=96.0
        self.label_2.setText(str(a))
        font = self.label_2.font()
        font.setPointSize(26)
        font.setBold(True)
        self.label_2.setFont(font)
        changechannel(960)
        
    def changechannel98(self):
        a=98.0
        self.label_2.setText(str(a))
        font = self.label_2.font()
        font.setPointSize(26)
        font.setBold(True)
        self.label_2.setFont(font)
        changechannel(980)
        
    def changechannel101(self):
        a=101.0
        self.label_2.setText(str(a))
        font = self.label_2.font()
        font.setPointSize(26)
        font.setBold(True)
        self.label_2.setFont(font)
        changechannel(1011)
        
    
    def volumeUp(self):
        if(self.currvol>=10):
            return
        self.currvol += 1
        setvolume (self.currvol)
        self.label_3.setText("Volume "+str(self.currvol))
        font = self.label_3.font()
        font.setPointSize(12)
        self.label_3.setFont(font)
    def volumeDown(self):
        if(self.currvol<=1):
            return
        self.currvol -= 1
        setvolume (self.currvol)
        self.label_3.setText("Volume "+str(self.currvol))
        font = self.label_3.font()
        font.setPointSize(12)
        self.label_3.setFont(font)
    def playPause(self):
        if (self.playPauseS == True):
            self.playPauseS=False
            setvolume(0)
            self.pushButton_3.setIcon(QIcon("Images/pause.png"))
            
        else:
            self.playPauseS=True
            setvolume(currvol)
            self.pushButton_3.setIcon(QIcon("Images/play.png"))
    
    def setupUi(self, Radio):
        self.playPauseS = True
        self.currvol=7
        Radio.setObjectName("Radio")
        Radio.resize(800, 600)
        Radio.setStyleSheet("background-color: rgb(67, 67, 67);")
        self.centralwidget = QtWidgets.QWidget(Radio)
        self.centralwidget.setObjectName("centralwidget")
        
        #Home Button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 81, 61))
        self.pushButton.setStyleSheet("background-color: rgb(32, 65, 98);")
        self.pushButton.setText("")
        self.pushButton.clicked.connect(self.BackHome) # 1 up
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(50, 50))
        self.pushButton.setObjectName("pushButton")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 60, 801, 431))
        self.frame.setStyleSheet("background-color: rgb(232, 232, 232);\n"
"border-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 255), stop:0.05 rgba(14, 8, 73, 255), stop:0.36 rgba(28, 17, 145, 255), stop:0.6 rgba(126, 14, 81, 255), stop:0.75 rgba(234, 11, 11, 255), stop:0.79 rgba(244, 70, 5, 255), stop:0.86 rgba(255, 136, 0, 255), stop:0.935 rgba(239, 236, 55, 255));\n"
"border-color: rgb(85, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        
        #Seek prev
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(70, 180, 93, 71))
        self.pushButton_2.setStyleSheet("background-color: rgb(57, 115, 173);")
        self.pushButton_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/backward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(80, 80))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.seekP) # 1 down
        
        
        #Play Pause
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 180, 93, 71))
        self.pushButton_3.setStyleSheet("background-color: rgb(32, 65, 98);")
        self.pushButton_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QtCore.QSize(60, 80))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.playPause)
        
        #Seek Next
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(250, 180, 93, 71))
        self.pushButton_4.setStyleSheet("background-color: rgb(57, 115, 173);")
        self.pushButton_4.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Images/forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setIconSize(QtCore.QSize(80, 80))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.seekN) # 1 up
        
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(70, 120, 271, 51))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("89.0")
        font = self.label_2.font()
        font.setPointSize(26)
        font.setBold(True)
        self.label_2.setFont(font)
        
        
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(440, 20, 321, 381))
        self.frame_3.setStyleSheet("background-color: rgb(57, 115, 173);\n"
"border-color: qlineargradient(spread:pad, x1:0.333, y1:0.539773, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        
        #Go to 89.0
        self.pushButton_8 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_8.setGeometry(QtCore.QRect(0, 20, 321, 51))
        self.pushButton_8.setStyleSheet("background-color: rgb(38, 76, 115);\n"
"background-color: rgb(32, 65, 98);")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(self.changechannel89) # manuallly go to 89.0
        
        #Go to 91.0
        self.pushButton_12 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_12.setGeometry(QtCore.QRect(0, 90, 321, 51))
        self.pushButton_12.setStyleSheet("background-color: rgb(32, 65, 98);")
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_12.clicked.connect(self.changechannel91) # manuallly go to 91.0
        
        #Go to 98.0
        self.pushButton_9 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_9.setGeometry(QtCore.QRect(0, 240, 321, 51))
        self.pushButton_9.setStyleSheet("background-color: rgb(32, 65, 98);")
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.clicked.connect(self.changechannel98) # manuallly go to 98.0
        
        
        #Go to 101.0
        self.pushButton_10 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_10.setGeometry(QtCore.QRect(0, 310, 321, 51))
        self.pushButton_10.setStyleSheet("background-color: rgb(32, 65, 98);")
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.clicked.connect(self.changechannel101) # manuallly go to 101.1
        
        #Go to 96.0
        self.pushButton_14 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_14.setGeometry(QtCore.QRect(0, 160, 321, 51))
        self.pushButton_14.setStyleSheet("background-color: rgb(32, 65, 98);")
        self.pushButton_14.setObjectName("pushButton_14")
        self.pushButton_14.clicked.connect(self.changechannel96) # go to manuallly to 96.0
        
        #Volume Down
        self.pushButton_6 = QtWidgets.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(70, 320, 93, 61))
        self.pushButton_6.setStyleSheet("background-color: rgb(57, 115, 173);")
        self.pushButton_6.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Images/volume down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon4)
        self.pushButton_6.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.volumeDown) # volume down by 1
        
        
        # Volume Up
        self.pushButton_7 = QtWidgets.QPushButton(self.frame)
        self.pushButton_7.setGeometry(QtCore.QRect(280, 317, 93, 61))
        self.pushButton_7.setStyleSheet("background-color: rgb(57, 115, 173);")
        self.pushButton_7.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Images/volumeup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon5)
        self.pushButton_7.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.volumeUp) # volume up by 1
        
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(170, 320, 100, 70))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Volume "+str(self.currvol))
        font = self.label_3.font()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.TitleFrame = QtWidgets.QFrame(self.centralwidget)
        self.TitleFrame.setGeometry(QtCore.QRect(80, 0, 721, 61))
        self.TitleFrame.setAutoFillBackground(False)
        self.TitleFrame.setStyleSheet("color: rgb(17, 17, 17);\n"
"background-color: rgb(57, 115, 173);\n"
"\n"
"")
        self.TitleFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TitleFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TitleFrame.setObjectName("TitleFrame")
        self.label = QtWidgets.QLabel(self.TitleFrame)
        self.label.setGeometry(QtCore.QRect(10, 0, 231, 51))
        self.label.setObjectName("label")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 490, 801, 61))
        self.frame_2.setStyleSheet("background-color: rgb(57, 115, 173);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        
        # Back Home
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_5.setGeometry(QtCore.QRect(700, 0, 101, 61))
        self.pushButton_5.setStyleSheet("background-color: rgb(32, 65, 98);")
        self.pushButton_5.setText("")
        self.pushButton_5.clicked.connect(self.BackHome) # 1 up
        
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Images/backhome.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon6)
        self.pushButton_5.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(30, 0, 621, 61))
        self.label_4.setObjectName("label_4")
        Radio.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Radio)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        Radio.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Radio)
        self.statusbar.setObjectName("statusbar")
        Radio.setStatusBar(self.statusbar)

        self.retranslateUi(Radio)
        QtCore.QMetaObject.connectSlotsByName(Radio)

    def retranslateUi(self, Radio):
        _translate = QtCore.QCoreApplication.translate
        Radio.setWindowTitle(_translate("Radio", "MainWindow"))
        #self.label_2.setText(_translate("Radio", "<html><head/><body><p><span style=\" font-size:26pt; color:#000000;\">106.0</span></p></body></html>"))
        self.pushButton_8.setText(_translate("Radio", "89.0"))
        self.pushButton_12.setText(_translate("Radio", "91.0"))
        self.pushButton_9.setText(_translate("Radio", "98.0"))
        self.pushButton_10.setText(_translate("Radio", "101.0"))
        self.pushButton_14.setText(_translate("Radio", "96.0"))
        #self.label_3.setText(_translate("Radio", "<html><head/><body><p><span style=\" color:#000000;\">Volume 0</span></p></body></html>"))
        self.label.setText(_translate("Radio", "<html><head/><body><p><span style=\" font-size:22pt; font-weight:600; color:#ffffff;\">FM Radio</span></p></body></html>"))
        self.label_4.setText(_translate("Radio", "<html><head/><body><p><span style=\" font-size:22pt;\">Radio FM Pakistan</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Radio = QtWidgets.QMainWindow()
    ui = Ui_Radio()
    ui.setupUi(Radio)
    Radio.show()
    sys.exit(app.exec_())
