import os
import subprocess
from test1 import VideoWindow
from phone import PhoneWindow
from Radio import Ui_Radio
from bluetooth import BWindow
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QStandardPaths, QModelIndex
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer,QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QDialog, QListWidget,
                             QFrame, QListWidgetItem)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon, QFont, QColor
import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Smart Car")

        self.MediaPlayer= VideoWindow()
        self.MediaPlayer.setFixedSize(QSize(800, 410))
        self.RadioPlayer=Ui_Radio()
        self.RadioPlayer.setFixedSize(QSize(800, 410))
	self.BT=BWindow()
        self.BT.setFixedSize(QSize(800, 410))
	self.Phone=PhoneWindow()
        self.Phone.setFixedSize(QSize(800, 410))
        self.title=QLabel()

        self.musicmode=True

        self.MediaButton = QPushButton()
        self.playButton = QPushButton()
        self.nextButton = QPushButton()
        self.prevButton = QPushButton()

        self.RadioButton = QPushButton()
	self.NavigationButton = QPushButton()
        self.VoiceButton = QPushButton()
        self.CallButton = QPushButton()
        self.CameraButton = QPushButton()
        #self.tempButton = QPushButton()

        self.guiBuilder()
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        Hlayout0 = QHBoxLayout()
        Hlayout0.addWidget(self.title)
        Hlayout0.addWidget(self.prevButton)
        Hlayout0.addWidget(self.playButton )
        Hlayout0.addWidget(self.nextButton)
        #Hlayout0.addWidget(self.CameraButton)
	
        Hlayout1 = QHBoxLayout()
        Hlayout1.addWidget(self.MediaButton)
        Hlayout1.addWidget(self.RadioButton)
        Hlayout1.addWidget(self.NavigationButton)
        Hlayout2 = QHBoxLayout()
        Hlayout2.addWidget(self.VoiceButton)
        Hlayout2.addWidget(self.CallButton)
        Hlayout2.addWidget(self.CameraButton )

        layout = QVBoxLayout()
        #layout.addWidget(self.title)
        layout.addLayout(Hlayout0)
        layout.addLayout(Hlayout1)
        layout.addLayout(Hlayout2)


        wid.setLayout(layout)
	wid.setStyleSheet("background-image: url(/home/pi/music2/img/back1.jpeg); background-attachment: fixed")
        self.MediaPlayer.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.MediaPlayer.videoPlaylist.currentMediaChanged.connect(self.mediaChanged)
        self.MediaPlayer.musicPlaylist.currentMediaChanged.connect(self.mediaChanged)
        self.MediaPlayer.next()

    def guiBuilder(self):
        p = self.palette()
        self.palette().setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.setStyleSheet("background-color:#2B2B2B")

        font1 = QFont("Bahnschrift SemiBold", 10)
        self.title.setFixedSize(780, 20)
        self.title.setStyleSheet("color:#F4F8F7")
        self.title.setFont(font1)

        self.MediaButton.setIcon(QIcon('/home/pi/music2/img/music1.png'))
        self.MediaButton.setIconSize(QSize(150, 180))
        self.MediaButton.clicked.connect(self.MediaPlay)
	self.MediaButton.setStyleSheet("background-image: url(/home/pi/music2/img/back.jpeg); background-attachment: fixed")
        

        self.RadioButton.setIcon(QIcon('/home/pi/music2/img/radio.png'))
        self.RadioButton.setIconSize(QSize(150, 180))
        self.RadioButton.clicked.connect(self.RadioPlay)
	self.RadioButton.setStyleSheet("background-image: url(/home/pi/music2/img/back.jpeg); background-attachment: fixed")
        

        self.NavigationButton.setIcon(QIcon('/home/pi/music2/img/map.png'))
        self.NavigationButton.setIconSize(QSize(150, 180))
        self.NavigationButton.clicked.connect(self.navit)
	self.NavigationButton.setStyleSheet("background-image: url(/home/pi/music2/img/back.jpeg); background-attachment: fixed")
        

        self.VoiceButton.setIcon(QIcon('/home/pi/music2/img/bluetooth.png'))
        self.VoiceButton.setIconSize(QSize(150, 180))
        self.VoiceButton.clicked.connect(self.openBluetooth)
        self.VoiceButton.setStyleSheet("background-image: url(/home/pi/music2/img/back.jpeg); background-attachment: fixed")
        

        self.CallButton.setIcon(QIcon('/home/pi/music2/img/dial.png'))
        self.CallButton.setIconSize(QSize(150, 180))
        self.CallButton.clicked.connect(self.openPhone)
	self.CallButton.setStyleSheet("background-image: url(/home/pi/music2/img/back.jpeg); background-attachment: fixed")
        

        #self.tempButton.setIcon(QIcon('/home/pi/music2/img/camera1.png'))
        #self.tempButton.setIconSize(QSize(150, 180))
        #self.CameraButton.clicked.connect(self.play)
	#self.tempButton.setStyleSheet("background-image: url(/home/pi/music2/img/back.jpeg); background-attachment: fixed")
        

        self.playButton.setIcon(QIcon('/home/pi/music2/img/play_circle.png'))
        self.playButton.setIconSize(QSize(30, 30))
        self.playButton.clicked.connect(self.Play)

        self.prevButton.setIcon(QIcon('/home/pi/music2/img/skip_previous.png'))
        self.prevButton.setIconSize(QSize(30, 30))
        self.prevButton.clicked.connect(self.MediaPlayer.prev)

        self.nextButton.setIcon(QIcon('/home/pi/music2/img/skip_next.png'))
        self.nextButton.setIconSize(QSize(30, 30))
        self.nextButton.clicked.connect(self.MediaPlayer.next)

        self.CameraButton.setIcon(QIcon('/home/pi/music2/img/camera2.png'))
        self.CameraButton.setIconSize(QSize(150, 180))
        self.CameraButton.clicked.connect(self.openCamera)
	self.CameraButton.setStyleSheet("background-image: url(/home/pi/music2/img/back.jpeg); background-attachment: fixed")
        
	
    def Play(self):
        self.RadioPlayer.setVolume(0)
        self.musicmode=True
        self.MediaPlayer.play()

    def MediaPlay(self):
        #if(self.musicmode==False):
        #self.RadioPlayer.setVolume(0)
        self.musicmode=True
        #print("ander")
        self.MediaPlayer.show()
        self.MediaPlayer.move(0,0)

    def RadioPlay(self):
        if self.MediaPlayer.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.musicmode=False
            self.MediaPlayer.mediaPlayer.pause()
        self.RadioPlayer.setVolume(50)
        self.RadioPlayer.show()
        self.RadioPlayer.move(0,0) 

    def openPhone(self):
        if self.MediaPlayer.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.musicmode=False
            self.MediaPlayer.mediaPlayer.pause()
        self.RadioPlayer.setVolume(0)
        self.Phone.show()
        self.Phone.move(0,0)

    def openBluetooth(self):
        if self.MediaPlayer.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.musicmode=False
            self.MediaPlayer.mediaPlayer.pause()
	self.RadioPlayer.setVolume(0)
        self.BT.show()
        self.BT.move(0,0)

    def navit(self):
        print("X")
        test = subprocess.Popen(["navit"], stdout=subprocess.PIPE)
        output = test.communicate()[0]

    def openCamera(self):
        os.system("LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 python3 /home/pi/music2/camera2.py")

    def mediaStateChanged(self, state):
        if self.MediaPlayer.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                QIcon('/home/pi/music2/img/pause_circle.png'))
            self.playButton.setIconSize(QSize(30, 30))
        else:
            self.playButton.setIcon(
                QIcon('/home/pi/music2/img/play_circle.png'))
            self.playButton.setIconSize(QSize(30, 30))
  
    def mediaChanged(self, media):
        if media:
            print(media.canonicalUrl().fileName())
            if(self.MediaPlayer.musicMode==True):
                if(self.MediaPlayer.musicplaylistdirectory==""):
                    self.title.setText(
                        "Now Playing : : " + media.canonicalUrl().fileName() + " || " + "Base Folder")
                else:
                    self.title.setText("Now Playing : : "+media.canonicalUrl().fileName() + " || "+self.MediaPlayer.musicplaylistdirectory[1:])
            else:
                if(self.MediaPlayer.videoplaylistdirectory==""):
                    self.title.setText(
                        "Now Playing : : " + media.canonicalUrl().fileName() + " || " + "Base Folder")
                else:
                    self.title.setText(
                        "Now Playing : : " + media.canonicalUrl().fileName() + " || " + self.MediaPlayer.videoplaylistdirectory[1:])
    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = MainWindow()
    Main.setFixedSize(QSize(800,410))
    Main.show()
    Main.move(0,0)
    sys.exit(app.exec_())




