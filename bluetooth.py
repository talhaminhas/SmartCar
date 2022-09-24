import os
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QStandardPaths, QModelIndex
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer,QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication,QLineEdit, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QDialog, QListWidget,
                             QFrame, QListWidgetItem)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon, QFont, QColor
import sys
#from media_control import media
import subprocess
 
class BWindow(QMainWindow):
    def __init__(self, parent=None):
        super(BWindow, self).__init__(parent)
        self.setWindowTitle("Dialer")
	#test = subprocess.Popen(["python /home/pi/music2/media_control.py"], stdout=subprocess.PIPE)
        #output = test.communicate()[0]
	#os.system("python media_control.py")
	#execfile('media_control.py')
	#self.media_nav= media()
        #self.setStyleSheet("{background-image: url(:/home/pi/music2/img/back.jpg);}")

        self.listFrame=QFrame()
        self.title=QLabel()

        self.contactlist = QListWidget()
        self.HomeButton = QPushButton()
        
        

        #Control Buttons
        self.playButton = QPushButton()
        self.nextButton = QPushButton()
        self.prevButton = QPushButton()
        self.volSlider = QSlider(Qt.Horizontal)
        self.muteButton = QPushButton()
        self.coverImage = QPushButton()
        
        self.infolist = QListWidget()

        self.guiBuilder()
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)
	wid.setStyleSheet("background-image: url(/home/pi/music2/img/back1.jpeg); background-attachment: fixed")
        
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(5, 0, 5, 5)
        controlLayout.addWidget(self.prevButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.nextButton)
        controlLayout.addWidget(self.volSlider)
        controlLayout.addWidget(self.muteButton)


        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(5, 0, 5, 5)
        
        topLayout.addWidget(self.title)
        topLayout.addWidget(self.HomeButton)

        listLayout = QHBoxLayout()
        listLayout.addWidget(self.infolist)
        listLayout.addWidget(self.coverImage)
        self.listFrame.setLayout(listLayout)
        self.listFrame.setFixedSize(QSize(800,300))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(topLayout)
        
        layout.addWidget(self.listFrame)
        layout.addLayout(controlLayout)

        # Set widget to contain window contents
        wid.setLayout(layout)

    def guiBuilder(self):
        p = self.palette()
        self.palette().setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.setStyleSheet("background-color:#000000")

        font1 = QFont("Bahnschrift SemiBold", 20)
        self.title.setFixedSize(780, 40)
        self.title.setStyleSheet("color:#F4F8F7")
        self.title.setFont(font1)
        self.title.setText("Bluetooth Music")
        self.title.setAlignment(Qt.AlignHCenter)
        
        font2 = QFont("Bahnschrift SemiBold", 13)
        self.contactlist.setStyleSheet("color:#F4F8F7")
        self.infolist.setVisible(True)
        self.infolist.setFixedSize(430,280)
        self.infolist.setFont(font2)
        #self.infolist.clicked.connect(self.contactClick)
        self.infolist.addItem("Title\nBay Parwah \n")
        self.infolist.addItem("Aritist\nImran Khan and Bohemia\n")
        self.infolist.addItem("Album\nSchool di Kitab\n")
        #self.contactlist.clicked.connect(self.listclicked)

        
        self.HomeButton.setIcon(QIcon('/home/pi/music2/img/home.png'))
        self.HomeButton.setIconSize(QSize(25, 25))
        self.HomeButton.clicked.connect(self.homeclick)
        
        self.coverImage.setIcon(
            QIcon('/home/pi/music2/img/music.png'))
        self.coverImage.setIconSize(QSize(280, 280))
        
        self.playButton.setIcon(QIcon('/home/pi/music2/img/play_circle.png'))
        self.playButton.setIconSize(QSize(30, 30))
        self.playButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        #self.playButton.clicked.connect(self.play)
        
        self.muteButton.setIcon(QIcon('/home/pi/music2/img/unmute.png'))
        self.muteButton.setIconSize(QSize(30, 30))
        #self.muteButton.clicked.connect(self.mute)
        
        self.nextButton.setIcon(QIcon('/home/pi/music2/img/skip_next.png'))
        self.nextButton.setIconSize(QSize(30, 30))
        #self.nextButton.clicked.connect(next)

        self.prevButton.setIcon(QIcon('/home/pi/music2/img/skip_previous.png'))
        self.prevButton.setIconSize(QSize(30, 30))
        #self.prevButton.clicked.connect(self.prev)
        
        self.volSlider.setRange(0, 100)
        self.volSlider.setValue(50)

    def homeclick(self):
        self.hide()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    player = BWindow()
    player.setFixedSize(QSize(800,480))
    player.show()
  

    sys.exit(app.exec_())




   
    