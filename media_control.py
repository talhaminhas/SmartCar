
import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
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
#image_url = "/home/pi/music2/img/album.png"
URL = 'https://www.google.com/search?tbm=isch&q='
HEADER = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
viewer = None

class media(QMainWindow):
	def on_property_changed(self,interface, changed, invalidated):
	    '''if interface != 'org.bluez.MediaPlayer1':
		return
	    for prop, value in changed.items():
		if prop == 'Status':
		    print('Playback Status: {}'.format(value))
		elif prop == 'Track':
		    print('Music Info:')
		    for key in ('Title', 'Artist', 'Album'):
		        print('   {}: {}'.format(key, value.get(key, '')))
		    #show_album_art(value.get('Artist', ''), value.get('Album', ''))'''
	 
	def on_playback_control(self,fd, condition):
	    '''str = fd.readline()
	    if str.startswith('play'):
		player_iface.Play()
	    elif str.startswith('pause'):
		player_iface.Pause()
	    elif str.startswith('next'):
		player_iface.Next()
	    elif str.startswith('prev'):
		player_iface.Previous()'''
	    return True

	def __init__(self , parent=None):

            super(media, self).__init__(parent)
            self.setWindowTitle("Dialer")
	    #test = subprocess.Popen(["python /home/pi/music2/media_control.py"], stdout=subprocess.PIPE)
            #output = test.communicate()[0]
	    #os.system("python media_control.py")
	    #execfile('media_control.py')
	    #self.media_nav= media()

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

            #self.guiBuilder()
            # Create a widget for window contents
            wid = QWidget(self)
            self.setCentralWidget(wid)
        
            controlLayout = QHBoxLayout()
            controlLayout.setContentsMargins(5, 0, 5, 5)
            controlLayout.addWidget(self.prevButton)
            controlLayout.addWidget(self.playButton)
            controlLayout.addWidget(self.nextButton)
            controlLayout.addWidget(self.volSlider)
            controlLayout.addWidget(self.muteButton)


            topLayout = QHBoxLayout()
            topLayout.setContentsMargins(5, 5, 5, 0)
        
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
       
	    '''dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	    bus = dbus.SystemBus()
	    obj = bus.get_object('org.bluez', "/")
	    mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
	    for path, ifaces in mgr.GetManagedObjects().items():
		adapter = ifaces.get('org.bluez.MediaPlayer1')
		if not adapter:
		    continue
		player = bus.get_object('org.bluez',path)
		player_iface = dbus.Interface(
		        player,
		        dbus_interface='org.bluez.MediaPlayer1')
		break
	    if not adapter:
		sys.exit('Error: Media Player not found.')
	 
	    bus.add_signal_receiver(
		    self.on_property_changed,
		    bus_name='org.bluez',
		    signal_name='PropertiesChanged',
		    dbus_interface='org.freedesktop.DBus.Properties')
	    GLib.io_add_watch(sys.stdin, GLib.IO_IN, self.on_playback_control)
	    GLib.MainLoop().run()'''
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
            self.infolist.addItem("Title\n03459268135\n")
            self.infolist.addItem("Aritist\n03459268134\n")
            self.infolist.addItem("Album\n0315579969\n")
            #self.contactlist.clicked.connect(self.listclicked)

        
            self.HomeButton.setIcon(QIcon('/home/pi/music2/img/home.png'))
            self.HomeButton.setIconSize(QSize(25, 25))
            self.HomeButton.clicked.connect(self.homeclick)
        
            self.coverImage.setIcon(QIcon('/home/pi/music2/img/music.png'))
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
            #self.nextButton.clicked.connect(self.next)

            self.prevButton.setIcon(QIcon('/home/pi/music2/img/skip_previous.png'))
            self.prevButton.setIconSize(QSize(30, 30))
            #self.prevButton.clicked.connect(self.prev)
        
            self.volSlider.setRange(0, 100)
            self.volSlider.setValue(50)

        def homeclick(self):
            self.hide()

if __name__ == '__main__':
    #x=media()
    app = QApplication(sys.argv)
    player = media()
    player.setFixedSize(QSize(800,480))
    player.show()
    sys.exit(app.exec_())





