import os
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QStandardPaths, QModelIndex
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer,QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QDialog, QListWidget,
                             QFrame, QListWidgetItem)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon, QFont, QColor
import sys



class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Video Player")

        self.songsdirectory = "/home/pi/music2/Songs"
        self.basesongsdirectory = "/home/pi/music2/Songs"
        self.basevideodirectory = "/home/pi/music2/Videos"
        self.videodirectory = "/home/pi/music2/Videos"
        self.currentsongsdirectory = ""
        self.currentvideodirectory = ""
        self.musicplaylistdirectory = ""
        self.videoplaylistdirectory = ""
        self.currentsongindex = 0
        self.currentsongDindex = 0
        self.currentvideoindex = 0
        self.currentvideoDindex = 0
        self.videoPlaylist = QMediaPlaylist()
        self.musicPlaylist = QMediaPlaylist()
        self.listFrame=QFrame()
        self.musicMode=False
        self.listMode = False
        self.loadMusicPlaylist=True
        self.loadVideoPlaylist=True
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.title=QLabel()
        self.start = QLabel()
        self.end = QLabel()

        self.playButton = QPushButton()
        self.HomeButton = QPushButton()
        self.coverImage = QPushButton()
        self.muteButton = QPushButton()
        self.modeswitchButton = QPushButton()
        self.nextButton = QPushButton()
        self.prevButton = QPushButton()
        self.pageButton = QPushButton()
        self.showButton = QPushButton()
        self.shuffleButton = QPushButton()

        self.positionSlider = QSlider(Qt.Horizontal)
        self.volSlider = QSlider(Qt.Horizontal)

        self.songslist = QListWidget()
        self.songsfolderlist = QListWidget()
        self.videoslist = QListWidget()
        self.videosfolderlist = QListWidget()

        self.guiBuilder()
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(5, 5, 5, 0)
        
        topLayout.addWidget(self.title)
        topLayout.addWidget(self.HomeButton)

        # Create layouts to place inside widget
        progressLayout = QHBoxLayout()
        progressLayout.setContentsMargins(8, 0, 8, 0)
        progressLayout.addWidget(self.start)
        progressLayout.addWidget(self.positionSlider)
        progressLayout.addWidget(self.end)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(5, 0, 5, 5)
        controlLayout.addWidget(self.prevButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.nextButton)
        controlLayout.addWidget(self.volSlider)
        controlLayout.addWidget(self.muteButton)
        controlLayout.addWidget(self.pageButton)
        controlLayout.addWidget(self.modeswitchButton)

        listLayout = QHBoxLayout()
        listLayout.addWidget(self.songsfolderlist)
        listLayout.addWidget(self.videosfolderlist)
        listLayout.addWidget(self.songslist)
        listLayout.addWidget(self.videoslist)
        self.listFrame.setLayout(listLayout)
        self.listFrame.setFixedSize(QSize(800,300))
        self.listFrame.hide()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(topLayout)
        layout.addWidget(self.listFrame)
        layout.addWidget(self.videoWidget)

        layout.addWidget(self.coverImage)
        layout.addLayout(progressLayout)
        layout.addLayout(controlLayout)
        layout.addWidget(self.showButton)
        # Set widget to contain window contents
        wid.setLayout(layout)
	wid.setStyleSheet("background-image: url(/home/pi/music2/img/back1.jpeg); background-attachment: fixed")

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.volumeChanged.connect(self.mediaVolumeChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        self.videoPlaylist.currentMediaChanged.connect(self.mediaChanged)
        self.musicPlaylist.currentMediaChanged.connect(self.mediaChanged)

        os.chdir(self.songsdirectory)
        self.openSongs(True)
        self.loadMusic()
        os.chdir(self.videodirectory)
        self.openVideo(True)
        self.loadVideos()
        self.mediaPlayer.setPlaylist(self.videoPlaylist)

    def guiBuilder(self):
        p = self.palette()
        self.palette().setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.setStyleSheet("background-color:#000000")

        font1 = QFont("Bahnschrift SemiBold", 10)
        self.title.setFixedSize(780, 20)
        self.title.setStyleSheet("color:#F4F8F7")
        self.title.setFont(font1)

        self.videoWidget.setMinimumSize(720,100)

        self.start.setFixedSize(60, 20)
        self.start.setStyleSheet("color:#F4F8F7")
        self.start.setFont(font1)
        self.start.setText("--/--/--")

        self.end.setFixedSize(60, 20)
        self.end.setStyleSheet("color:#F4F8F7")
        self.end.setFont(font1)
        self.end.setText("--/--/--")

        font2 = QFont("Bahnschrift SemiBold", 15)
        self.songslist.setStyleSheet("color:#F4F8F7")
        self.songslist.setVisible(False)
        self.songslist.setFixedSize(530,280)
        self.songslist.setFont(font2)
        self.songslist.clicked.connect(self.listclicked)

        self.songsfolderlist.setStyleSheet("color:#F4F8F7")
        self.songsfolderlist.setVisible(False)
        self.songsfolderlist.setFixedSize(250,280)
        self.songsfolderlist.setFont(font2)
        self.songsfolderlist.clicked.connect(self.FolderClicked)
        self.songsfolderlist.addItem("Base Folder")

        self.videoslist.setStyleSheet("color:#F4F8F7")
        self.videoslist.setVisible(False)
        self.videoslist.setFixedSize(530,280)
        self.videoslist.setFont(font2)
        self.videoslist.clicked.connect(self.listclicked)

        self.videosfolderlist.setStyleSheet("color:#F4F8F7")
        self.videosfolderlist.setVisible(False)
        self.videosfolderlist.setFixedSize(250, 280)
        self.videosfolderlist.setFont(font2)
        self.videosfolderlist.clicked.connect(self.FolderClicked)
        self.videosfolderlist.addItem("Base Folder")

        self.playButton.setIcon(QIcon('/home/pi/music2/img/play_circle.png'))
        self.playButton.setIconSize(QSize(30, 30))
        self.playButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        self.playButton.clicked.connect(self.play)

        self.HomeButton.setIcon(QIcon('/home/pi/music2/img/home.png'))
        self.HomeButton.setIconSize(QSize(25, 25))
        self.HomeButton.clicked.connect(self.homeclick)

        self.showButton.setIcon(QIcon('/home/pi/music2/img/grid.png'))
        self.showButton.setIconSize(QSize(10, 10))
        self.showButton.setVisible(False)
        #self.playButton.clicked.connect(self.play)

        self.muteButton.setIcon(QIcon('/home/pi/music2/img/unmute.png'))
        self.muteButton.setIconSize(QSize(30, 30))
        self.muteButton.clicked.connect(self.mute)

        self.coverImage.setIcon(
            QIcon('/home/pi/music2/img/music.png'))
        self.coverImage.setVisible(False)
        self.coverImage.setIconSize(QSize(280, 280))

        self.modeswitchButton.setIcon(QIcon('/home/pi/music2/img/now_playing.png'))
        self.modeswitchButton.setIconSize(QSize(30, 30))
        self.modeswitchButton.clicked.connect(self.modeswitch)

        self.pageButton.setIcon(QIcon('/home/pi/music2/img/list.png'))
        self.pageButton.setIconSize(QSize(30, 30))
        self.pageButton.clicked.connect(self.pageswitch)

        self.nextButton.setIcon(QIcon('/home/pi/music2/img/skip_next.png'))
        self.nextButton.setIconSize(QSize(30, 30))
        self.nextButton.clicked.connect(self.next)

        self.prevButton.setIcon(QIcon('/home/pi/music2/img/skip_previous.png'))
        self.prevButton.setIconSize(QSize(30, 30))
        self.prevButton.clicked.connect(self.prev)

        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.shuffleButton.setIcon(QIcon('/home/pi/music2/img/shuffle_off.png'))
        self.shuffleButton.setIconSize(QSize(30, 30))
        self.shuffleButton.resize(100, 32)
        self.shuffleButton.move(50, 50)
        self.shuffleButton.clicked.connect(self.fullScreen)

        self.volSlider.setRange(0, 100)
        self.volSlider.sliderMoved.connect(self.setVolume)
        self.mediaPlayer.setVolume(50)
        self.volSlider.setValue(50)
    def openSongs(self,folder):
        if (self.songsdirectory):
            self.songslist.clear()
            self.loadMusicPlaylist=True
            for files in os.listdir(self.songsdirectory):
                try:
                    if(os.path.isdir(files) and folder):
                        i = QListWidgetItem(files)
                        self.songsfolderlist.addItem(i)
                    if files.endswith(".mp3"):
                        i = QListWidgetItem(files)
                        self.songslist.addItem(i)
                except:
                    print(files + " is not a song")
        if(folder==True):
            self.songsfolderlist.setCurrentRow(self.currentsongDindex)
            #i = self.songsfolderlist.currentItem()
            #i.setBackground(QColor('#595B5D'))
    def loadMusic(self):
        self.musicplaylistdirectory=self.currentsongsdirectory
        if (self.songsdirectory):
            self.loadMusicPlaylist=False
            self.musicPlaylist.clear()
            for files in os.listdir(self.songsdirectory):
                try:
                    if files.endswith(".mp3"):
                        self.musicPlaylist.addMedia(QMediaContent(QUrl.fromLocalFile(
                            self.songsdirectory+"/"+files)))
                except:
                    print(files + " is not a song")
        self.musicPlaylist.setCurrentIndex(0)
        self.songslist.setCurrentRow(0)
        #i = self.songslist.item(0)
        #i.setBackground(QColor('#595B5D'))
    def openVideo(self,folder):
        if (self.videodirectory):
            self.videoslist.clear()
            self.loadVideoPlaylist=True
            for files in os.listdir(self.videodirectory):
                try:
                    if (os.path.isdir(files) and folder):
                        self.videosfolderlist.addItem(files)
                    if files.endswith(".mp4"):
                        self.videoslist.addItem(files)
                except:
                    print(files + " is not a video")
        if(folder==True):
            self.videoslist.setCurrentRow(1)
            self.videosfolderlist.setCurrentRow(self.currentvideoDindex)
            #i = self.videosfolderlist.currentItem()
            #i.setBackground(QColor('#595B5D'))
    def loadVideos(self):
        self.videoplaylistdirectory = self.currentvideodirectory
        if (self.videodirectory):
            self.loadVideoPlaylist = False
            self.videoPlaylist.clear()
            for files in os.listdir(self.videodirectory):
                try:
                    if files.endswith(".mp4"):
                        self.videoPlaylist.addMedia(QMediaContent(QUrl.fromLocalFile(
                            self.videodirectory+"/"+files)))
                except:
                    print(files + " is not a song")
        self.videoPlaylist.setCurrentIndex(0)
        self.videoslist.setCurrentRow(0)
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    def modeswitch(self):
        if self.musicMode == False:
            #os.chdir(self.songsdirectory+self.musicplaylistdirectory)
            self.setWindowTitle("Music Player")
            self.musicMode=True
            self.currentvideoindex=self.videoPlaylist.currentIndex()
            self.mediaPlayer.setPlaylist(self.musicPlaylist)
            self.musicPlaylist.setCurrentIndex(self.currentsongindex)
            self.mediaPlayer.play()
            self.modeswitchButton.setIcon(
                QIcon('/home/pi/music2/img/movie.png'))
            if self.listMode == True:
                self.listFrame.show()
                self.songslist.setVisible(True)
                self.songsfolderlist.setVisible(True)
                self.videoslist.setVisible(False)
                self.videosfolderlist.setVisible(False)
            else:
                self.videoWidget.setVisible(False)
                self.coverImage.setVisible(True)
        else:
            #os.chdir(self.videodirectory+self.videoplaylistdirectory)
            self.setWindowTitle("Video Player")
            self.musicMode = False
            self.currentsongindex = self.musicPlaylist.currentIndex()
            self.mediaPlayer.setPlaylist(self.videoPlaylist)
            self.videoPlaylist.setCurrentIndex(self.currentvideoindex)
            self.mediaPlayer.play()
            self.modeswitchButton.setIcon(
                QIcon('/home/pi/music2/img/now_playing.png'))
            if self.listMode == True:
                self.listFrame.show()
                self.songslist.setVisible(False)
                self.songsfolderlist.setVisible(False)
                self.videosfolderlist.setVisible(True)
                self.videoslist.setVisible(True)
            else:
                self.videoWidget.setVisible(True)
                self.coverImage.setVisible(False)
    def pageswitch(self):
        if self.listMode == False:
            self.listFrame.show()
            self.listMode=True
            self.pageButton.setIcon(QIcon('/home/pi/music2/img/tv1.png'))
            self.pageButton.setIconSize(QSize(30, 30))
            if(self.musicMode==False):
                self.videoslist.setVisible(True)
                self.videosfolderlist.setVisible(True)
                self.videoWidget.setVisible(False)
            else:
                self.songslist.setVisible(True)
                self.songsfolderlist.setVisible(True)
                self.coverImage.setVisible(False)
        else:
            self.listFrame.hide()
            self.pageButton.setIcon(QIcon('/home/pi/music2/img/list.png'))
            self.pageButton.setIconSize(QSize(30, 30))
            self.listMode = False
            if (self.musicMode == False):
                self.videoslist.setVisible(False)
                self.videosfolderlist.setVisible(False)
                self.videoWidget.setVisible(True)
            else:
                self.songslist.setVisible(False)
                self.songsfolderlist.setVisible(False)
                self.coverImage.setVisible(True)
    def fullScreen(self):
        self.title.setVisible(False)
        self.positionSlider.setVisible(False)
    def next(self):
        if self.musicMode == False:
            if(self.videoPlaylist.currentIndex()+1 < self.videoPlaylist.mediaCount()):
                #os.chdir(self.videodirectory + self.videoplaylistdirectory)
                self.videoPlaylist.next()
                #i = self.videoslist.currentItem()
                #i.setBackground(QColor('#000000'))
                self.videoslist.setCurrentRow(self.videoPlaylist.currentIndex())
                #i = self.videoslist.currentItem()
                #i.setBackground(QColor('#595B5D'))
            else:
                #i = self.videoslist.currentItem()
                #i.setBackground(QColor('#000000'))
                self.videoPlaylist.setCurrentIndex(0)
                self.videoslist.setCurrentRow(self.videoPlaylist.currentIndex())
                #i = self.videoslist.currentItem()
                #i.setBackground(QColor('#595B5D'))

        else:
            if (self.musicPlaylist.currentIndex() + 1 < self.musicPlaylist.mediaCount()):
                #os.chdir(self.songsdirectory + self.musicplaylistdirectory)
                self.musicPlaylist.next()
                #i=self.songslist.currentItem()
                #i.setBackground(QColor('#000000'))
                self.songslist.setCurrentRow(self.musicPlaylist.currentIndex())
                #i = self.songslist.currentItem()
                #i.setBackground(QColor('#595B5D'))
            else:
                #i = self.songslist.currentItem()
                #i.setBackground(QColor('#000000'))
                self.musicPlaylist.setCurrentIndex(0)
                self.songslist.setCurrentRow(self.musicPlaylist.currentIndex())
                #i = self.songslist.currentItem()
                #i.setBackground(QColor('#595B5D'))
    def prev(self):
        if self.musicMode == False:
            if (self.videoPlaylist.currentIndex() -1>=0):
                #os.chdir(self.videodirectory + self.videoplaylistdirectory)
                self.videoPlaylist.previous()
                #i = self.videoslist.currentItem()
                #i.setBackground(QColor('#000000'))
                self.videoslist.setCurrentRow(self.videoPlaylist.currentIndex())
                #i = self.videoslist.currentItem()
                #i.setBackground(QColor('#595B5D'))
            else:
                #i = self.videoslist.currentItem()
                #i.setBackground(QColor('#000000'))
                self.videoPlaylist.setCurrentIndex( self.videoPlaylist.mediaCount()-1)
                self.videoslist.setCurrentRow(self.videoPlaylist.currentIndex())
                #i = self.videoslist.currentItem()
                #i.setBackground(QColor('#595B5D'))
        else:
            if (self.musicPlaylist.currentIndex() -1>= 0):
                #os.chdir(self.songsdirectory + self.musicplaylistdirectory)
                self.musicPlaylist.previous()
                #i = self.songslist.currentItem()
                #i.setBackground(QColor('#000000'))
                self.songslist.setCurrentRow(self.musicPlaylist.currentIndex())
                #i = self.songslist.currentItem()
                #i.setBackground(QColor('#595B5D'))
            else:
                #i = self.songslist.currentItem()
                #i.setBackground(QColor('#000000'))
                self.musicPlaylist.setCurrentIndex(self.musicPlaylist.mediaCount()-1)
                self.songslist.setCurrentRow(self.musicPlaylist.currentIndex())
                #i = self.songslist.currentItem()
                #i.setBackground(QColor('#595B5D'))
    def mute(self):
        if self.mediaPlayer.isMuted() == True:
            self.mediaPlayer.setMuted(False)
            self.volSlider.setValue(self.mediaPlayer.volume())
            self.muteButton.setIcon(
                QIcon('/home/pi/music2/img/unmute.png'))
        else:
            self.mediaPlayer.setMuted(True)
            self.volSlider.setValue(0)
            self.muteButton.setIcon(
                QIcon('/home/pi/music2/img/mute.png'))
    def homeclick(self):
        self.hide()
    def FolderClicked(self):
        if (self.musicMode == True):
            print(self.basesongsdirectory)
            #i =self.songsfolderlist.item(self.currentsongDindex)
            #i.setBackground(QColor('#000000'))
            self.currentsongDindex=self.songsfolderlist.currentRow()
            #i = self.songsfolderlist.currentItem()
            #i.setBackground(QColor('#595B5D'))
            if(self.songsfolderlist.currentItem().text()=="Base Folder"):
                self.currentsongsdirectory=""
            else:
                self.currentsongsdirectory="/"+self.songsfolderlist.currentItem().text()
            self.songsdirectory=self.basesongsdirectory	+self.currentsongsdirectory
	    #os.chdir(self.songsdirectory+self.currentsongsdirectory)
            self.openSongs(False)
            if (self.currentsongsdirectory == self.musicplaylistdirectory):
                self.songslist.setCurrentRow(self.musicPlaylist.currentIndex())
                #i = self.songslist.currentItem()
                #i.setBackground(QColor('#595B5D'))
        else:
            #i = self.videosfolderlist.item(self.currentvideoDindex)
            #i.setBackground(QColor('#000000'))
            self.currentvideoDindex = self.videosfolderlist.currentRow()
            #i = self.videosfolderlist.currentItem()
            #i.setBackground(QColor('#595B5D'))
            if (self.videosfolderlist.currentItem().text() == "Base Folder"):
                self.currentvideodirectory = ""
            else:
                self.currentvideodirectory = "/" + self.videosfolderlist.currentItem().text()
            self.videodirectory=self.basevideodirectory	+self.currentvideodirectory
            #os.chdir(self.videodirectory + self.currentvideodirectory)
            self.openVideo(False)
            if (self.currentvideodirectory == self.videoplaylistdirectory):
                self.videoslist.setCurrentRow(self.videoPlaylist.currentIndex())
                #i = self.videoslist.currentItem()
                #i.setBackground(QColor('#595B5D'))
    def listclicked(self):
        if(self.musicMode==True):
            if(self.loadMusicPlaylist==True):
                self.loadMusic()
            #i = self.songslist.item(self.musicPlaylist.currentIndex())
            #i.setBackground(QColor('#000000'))
            self.musicPlaylist.setCurrentIndex(self.songslist.currentRow())
            #i = self.songslist.currentItem()
            #i.setBackground(QColor('#595B5D'))
        else:
            if(self.loadVideoPlaylist==True):
                self.loadVideos()
            #i = self.videoslist.item(self.videoPlaylist.currentIndex())
            #i.setBackground(QColor('#000000'))
            self.videoPlaylist.setCurrentIndex(self.videoslist.currentRow())
            #i = self.videoslist.currentItem()
            #i.setBackground(QColor('#595B5D'))
        self.mediaPlayer.play()
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                QIcon('/home/pi/music2/img/pause_circle.png'))
            self.playButton.setIconSize(QSize(30, 30))
        else:
            self.playButton.setIcon(
                QIcon('/home/pi/music2/img/play_circle.png'))
            self.playButton.setIconSize(QSize(30, 30))
    def mediaVolumeChanged(self, state):
        if self.mediaPlayer.volume()==0:
            self.muteButton.setIcon(
                QIcon('/home/pi/music2/img/mute.png'))
        else:
            self.muteButton.setIcon(
                QIcon('/home/pi/music2/img/unmute.png'))
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        millis = int(position)
        shours, sminutes, sseconds = self.convertTime(millis)
        self.start.setText(shours + ":" + sminutes + ":" + sseconds)
    def convertTime(self,millis):
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24
        shours = str(int(hours))
        sseconds = str(seconds)
        sminutes = str(minutes)
        if (hours < 10):
            shours = "0" + str(int(hours))
        if (seconds < 10):
            sseconds = "0" + str(seconds)
        if (minutes < 10):
            sminutes = "0" + str(minutes)
        return shours,sminutes,sseconds
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        millis = int(duration)
        shours,sminutes,sseconds = self.convertTime(millis)
        self.end.setText(shours+":"+sminutes+":"+sseconds)
    def mediaChanged(self, media):
        if media:
            print(media.canonicalUrl().fileName())
            if(self.musicMode==True):
                self.songslist.setCurrentRow(self.musicPlaylist.currentIndex())
                if(self.musicplaylistdirectory==""):
                    self.title.setText(
                        "Now Playing : : " + media.canonicalUrl().fileName() + " || " + "Base Folder")
                else:
                    self.title.setText("Now Playing : : "+media.canonicalUrl().fileName() + " || "+self.musicplaylistdirectory[1:])
            else:
                self.videoslist.setCurrentRow(self.videoPlaylist.currentIndex())
                if(self.videoplaylistdirectory==""):
                    self.title.setText(
                        "Now Playing : : " + media.canonicalUrl().fileName() + " || " + "Base Folder")
                else:
                    self.title.setText(
                        "Now Playing : : " + media.canonicalUrl().fileName() + " || " + self.videoplaylistdirectory[1:])
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    def setVolume(self, volume):
         self.mediaPlayer.setVolume(volume)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.setFixedSize(QSize(800,480))
    player.show()
    sys.exit(app.exec_())
