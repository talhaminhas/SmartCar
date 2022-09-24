# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Radio.ui'
#
# Created by: PyQt5 UI code generator 5.13.2

######
#Radio Module Working Code 
#Python Version 2 code

# Many Thanks to Nathan Seidle at Sparkfun for his Arduino Code Example
import RPi.GPIO as GPIO
import smbus
import time
import subprocess
GPIO.setwarnings(False)

i2c = smbus.SMBus(1)      #use 0 for older RasPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)

#create #create 16 registers for SI4703
reg = [0] * 16
 
#Register Descriptions
DEVICEID = 0x00
CHIPID = 0x01
POWERCFG = 0x02
CHANNEL = 0x03
SYSCONFIG1 = 0x04
SYSCONFIG2 = 0x05
SYSCONFIG3 = 0x06
OSCILLATOR = 0x07
STATUSRSSI = 0x0A
READCHAN = 0x0B
RDSA = 0x0C
RDSB = 0x0D
RDSC = 0x0E
RDSD = 0x0F

z = "000000000000000"
 
si4703_addr = 0x10 #found using i2cdetect utility
 
#create list to write registers
#only need to write registers 2-7 and since first byte is in the write
# command then only need 11 bytes to write
writereg = [0] * 11
 
#read 32 bytes
readreg = [0] * 32
 
def write_registers():
    #starts writing at register 2
    #but first byte is in the i2c write command
    global writereg
    global reg
    global readreg
    cmd, writereg[0] = divmod(reg[2], 1<<8)
    writereg[1], writereg[2] = divmod(reg[3], 1<<8)
    writereg[3], writereg[4] = divmod(reg[4], 1<<8)
    writereg[5], writereg[6] = divmod(reg[5], 1<<8)
    writereg[7], writereg[8] = divmod(reg[6], 1<<8)
    writereg[9], writereg[10] = divmod(reg[7], 1<<8)
    w6 = i2c.write_i2c_block_data(si4703_addr, cmd, writereg)
    readreg[16] = cmd #readreg
    read_registers()
    return
 
def read_registers():
    global readreg
    global reg
    readreg = i2c.read_i2c_block_data(si4703_addr, readreg[16], 32)
    #print("read reg ",readreg)
    reg[10] = readreg[0] * 256 + readreg[1]
    reg[11] = readreg[2] * 256 + readreg[3]
    reg[12] = readreg[4] * 256 + readreg[5]
    reg[13] = readreg[6] * 256 + readreg[7]
    reg[14] = readreg[8] * 256 + readreg[9]
    reg[15] = readreg[10] * 256 + readreg[11]
    reg[0] = readreg[12] * 256 + readreg[13]
    reg[1] = readreg[14] * 256 + readreg[15]
    reg[2] = readreg[16] * 256 + readreg[17]
    reg[3] = readreg[18] * 256 + readreg[19]
    reg[4] = readreg[20] * 256 + readreg[21]
    reg[5] = readreg[22] * 256 + readreg[23]
    reg[6] = readreg[24] * 256 + readreg[25]
    reg[7] = readreg[26] * 256 + readreg[27]
    reg[8] = readreg[28] * 256 + readreg[29]
    reg[9] = readreg[30] * 256 + readreg[31]
    return

def getchannel():
    read_registers()
    channel = reg[READCHAN] & 0x03FF
    channel *= 2
    channel += 875
    return channel
 
def changechannel(newchannel):
    if newchannel < 878 or newchannel > 1080:
       return
    global reg
    newchannel *= 10
    newchannel -= 8750
    newchannel /= 20
    read_registers()
    reg[CHANNEL] &= 0xFE00; #Clear out the channel bits
    reg[CHANNEL] |= newchannel; #Mask in the new channel
    reg[CHANNEL] |= (1<<15); #Set the TUNE bit to start
    write_registers()
    while 1:
    	read_registers()
    	if ((reg[STATUSRSSI] & (1<<14)) != 0):
        	break
    reg[CHANNEL] &= ~(1<<15)
    write_registers()
    return

def setvolume(newvolume):
    global reg
    if newvolume > 15:
        newvolume = 15
    if newvolume < 0:
        newvolume = 0
    read_registers()
    reg[SYSCONFIG2] &= 0xFFF0 #Clear volume bits
    reg[SYSCONFIG2] = newvolume #Set volume to lowest
    write_registers()
    return

def init():
    # init code needs to activate 2-wire (i2c) mode
    # the si4703 will not show up in i2cdetect until
    # you do these steps to put it into 2-wire (i2c) mode
   
    GPIO.output(2,GPIO.LOW)
    time.sleep(.1)
    GPIO.output(23, GPIO.LOW)
    time.sleep(.1)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(.1)
    subprocess.check_output(['gpio', '-g', 'mode', '2', 'ALT0'])

    read_registers()
    # do init step, turn on oscillator
    reg[OSCILLATOR] = 0x8100
    write_registers()
    time.sleep(1)

    read_registers()
    reg[POWERCFG] = 0x4001 #Enable the Radio IC and turn off muted
    write_registers()
    time.sleep(.1)

    read_registers()
    reg[SYSCONFIG1] |= (1<<12) #Enable RDS
    reg[SYSCONFIG2] &= 0xFFF0; #Clear volume bits
    #reg[SYSCONFIG2] = 0x0000; #Set volume to lowest
    #reg[SYSCONFIG3] = 0x0100; #Set extended volume range (too loud for me without this)
    write_registers()
    time.sleep(0.11)
    return

def seek(direction):
    read_registers()
    reg[POWERCFG] |= (1<<10 )
    if direction == 0:
        reg[POWERCFG] &= ~(1<<1)
    else:
        reg[POWERCFG] |= (1<<9)
    reg[POWERCFG] |= (1<<8)
    write_registers()
    while 1:
        read_registers()
        if ((reg[STATUSRSSI] & (1<<14)) != 0):
            break
    #print "Trying Station ", float(float(getchannel())/float(10))
    read_registers()
    valuesfbl = reg[STATUSRSSI] & (1<<13)
    reg[POWERCFG] &= ~(1<<8)
    write_registers()
    return

init() #init stuff

changechannel(890) #89.0 
setvolume(0)

#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
######
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QSlider, QListWidget, QWidget, QHBoxLayout, \
    QVBoxLayout, QFrame, QListWidgetItem
## Radio Code


def restore(settings):
    finfo = QFileInfo(settings.fileName())
    if finfo.exists() and finfo.isFile():
        for w in qApp.allWidgets():
            mo = w.metaObject()
            if w.objectName() != "":
                for i in range(mo.propertyCount()):
                    name = mo.property(i).name()
                    val = settings.value("{}/{}".format(w.objectName(), name), w.property(name))
                    w.setProperty(name, val)

def save(settings):
    for w in qApp.allWidgets():
        mo = w.metaObject()
        if w.objectName() != "":
            for i in range(mo.propertyCount()):
                name = mo.property(i).name()
                settings.setValue("{}/{}".format(w.objectName(), name), w.property(name))

#def getchannel():
 #   return 76.7
#def setvolume(a):
 #   print("setting volume ",a)
    
#def seek(a):
 #   print("seeking",a)
#def changechannel(a):
    
   # print("changing channel", a)

class Ui_Radio(QMainWindow):
    settings = QSettings("Radio.py", QSettings.IniFormat)
    def __init__(self, parent=None):
        super(Ui_Radio, self).__init__(parent)
        self.setWindowTitle("Radio")

        self.frequency = 880
        self.vol = 50
        self.playing = True
        self.mutestate = False
        self.listMode = False
        self.Gvol=0
        self.title = QLabel()
        self.start = QLabel()
        self.end = QLabel()
        self.volume = QLabel()

        self.listFrame = QFrame()

        self.playButton = QPushButton()
        self.HomeButton = QPushButton()
        self.muteButton = QPushButton()
        self.nextButton = QPushButton()
        self.prevButton = QPushButton()
        self.pageButton = QPushButton()
        self.coverImage = QPushButton()
        self.saveButton = QPushButton()

        self.positionSlider = QSlider(Qt.Horizontal)
        self.volSlider = QSlider(Qt.Horizontal)

        self.channelslist = QListWidget()

        self.guiBuilder()

        with open('/home/pi/music2/chanel.txt') as f:
            lines = f.readlines()
            lines = [line.rstrip('\n') for line in open('/home/pi/music2/chanel.txt')]
            for x in lines:
                print(x)
                if (x=="" or x=="\n"):
                    pass
                else:

                    i = QListWidgetItem(str(x))
                    i.setTextAlignment(Qt.AlignCenter)
                    self.channelslist.addItem(i)

        wid = QWidget(self)
        self.setCentralWidget(wid)
	wid.setStyleSheet("background-image: url(/home/pi/music2/img/back1.jpeg); background-attachment: fixed")

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
        controlLayout.addWidget(self.volume)
        controlLayout.addWidget(self.volSlider)
        controlLayout.addWidget(self.muteButton)
        controlLayout.addWidget(self.pageButton)
        controlLayout.addWidget(self.saveButton)

        listLayout = QHBoxLayout()
        listLayout.addWidget(self.channelslist)
        #listLayout.addWidget(self.frequency)
        self.listFrame.setLayout(listLayout)
        #self.listFrame.setFixedSize(QSize(780, 340))
        self.listFrame.hide()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(topLayout)
        #layout.addWidget(self.frequency)
        layout.addWidget(self.listFrame)
        layout.addWidget(self.coverImage)
        layout.addLayout(progressLayout)
        layout.addLayout(controlLayout)
        # Set widget to contain window contents
        wid.setLayout(layout)
	
    def guiBuilder(self):
        p = self.palette()
        self.palette().setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.setStyleSheet("background-color:#000001")  #99ceff

        font2 = QFont("Bahnschrift SemiBold", 35)
        self.title.setFixedSize(757, 50)
        self.title.setStyleSheet("color:#F4F8F7")
        self.title.setFont(font2)
        self.title.setText("FM 88.0")
        self.title.setAlignment(Qt.AlignCenter)

        font1 = QFont("Bahnschrift SemiBold", 10)
        self.start.setFixedSize(48, 20)
        self.start.setStyleSheet("color:#F4F8F7")
        self.start.setFont(font1)
        self.start.setText(" 88.00")

        self.end.setFixedSize(48, 20)
        self.end.setStyleSheet("color:#F4F8F7")
        self.end.setFont(font1)
        self.end.setText(" 108.00")

        self.volume.setFixedSize(48, 20)
        self.volume.setStyleSheet("color:#F4F8F7")
        self.volume.setFont(font1)
        self.volume.setText("  50%")

        font2 = QFont("Bahnschrift SemiBold", 25)
        self.channelslist.setStyleSheet("color:#F4F8F7")
        i = QListWidgetItem("89.0")
        i.setTextAlignment(Qt.AlignCenter)
        self.channelslist.addItem(i)
        i = QListWidgetItem("91.0")
        i.setTextAlignment(Qt.AlignCenter)
        self.channelslist.addItem(i)
        i = QListWidgetItem("96.0")
        i.setTextAlignment(Qt.AlignCenter)
        self.channelslist.addItem(i)
        i = QListWidgetItem("98.0")
        i.setTextAlignment(Qt.AlignCenter)
        self.channelslist.addItem(i)
        i = QListWidgetItem("101.0")
        i.setTextAlignment(Qt.AlignCenter)
        self.channelslist.addItem(i)
        #self.channelslist.setVisible(False)
        self.channelslist.setFont(font2)
        #self.songslist.clicked.connect(self.listclicked)



        self.channelslist.itemClicked.connect(self.favoriteChannels)
        
        
        
        self.playButton.setIcon(QIcon("/home/pi/music2/img/pause_circle.png"))
        self.playButton.setIconSize(QSize(30, 30))
        self.playButton.clicked.connect(self.play)

        self.muteButton.setIcon(QIcon("/home/pi/music2/img/unmute.png"))
        self.muteButton.setIconSize(QSize(30, 30))
        self.muteButton.clicked.connect(self.mute)

        self.saveButton.setIcon(QIcon('/home/pi/music2/img/save.png'))
        self.saveButton.setIconSize(QSize(25, 25))
        self.saveButton.clicked.connect(self.addChannel)

        self.nextButton.setIcon(QIcon('/home/pi/music2/img/skip_next.png'))
        self.nextButton.setIconSize(QSize(30, 30))
        self.nextButton.clicked.connect(self.next)

        self.pageButton.setIcon(QIcon('/home/pi/music2/img/list.png'))
        self.pageButton.setIconSize(QSize(30, 30))
        self.pageButton.clicked.connect(self.pageswitch)

        self.prevButton.setIcon(QIcon('/home/pi/music2/img/skip_previous.png'))
        self.prevButton.setIconSize(QSize(30, 30))
        self.prevButton.clicked.connect(self.prev)

        self.HomeButton.setIcon(QIcon('/home/pi/music2/img/home.png'))
        self.HomeButton.setIconSize(QSize(25, 25))
        self.HomeButton.clicked.connect(self.homeclick)

        self.coverImage.setIcon(
            QIcon('/home/pi/music2/img/radio.png'))
        self.coverImage.setIconSize(QSize(345, 345))

        self.positionSlider.setRange(880, 1080)
        self.positionSlider.setValue(880)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.volSlider.setRange(0, 100)
        self.volSlider.setValue(50)
        self.volSlider.sliderMoved.connect(self.setVolume)
    def BackHome(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_HomeMainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
    def setPosition(self, position):
        self.title.setText("FM "+str(position/10.0))
        self.frequency=position
        changechannel(self.frequency)
    def setVolume(self, position):
        self.vol=position
        self.volume.setText("   "+str(self.vol)+"%")
        a=self.vol/10
        #print(a)
        setvolume(a)
    def addChannel(self):
        a=self.frequency/10.0
        out = self.channelslist.findItems(str(a), QtCore.Qt.MatchExactly)
        if (len(out) == 0):
            i = QListWidgetItem(str(a))
            i.setTextAlignment(Qt.AlignCenter)
            self.channelslist.addItem(i)
            with open("chanel.txt", "a") as myfile:
    	        myfile.write(str(a)+'\n')
    def favoriteChannels(self):
        chanelNo=float(self.channelslist.currentItem().text())
        chanelNo=chanelNo*10
        chanelNo= int(chanelNo)
        #print (chanelNo)
        self.frequency=chanelNo
        self.title.setText("FM " + str(self.frequency / 10.0))
        self.positionSlider.setValue(chanelNo)
        changechannel(chanelNo)
    def next(self):
        if (self.frequency<1080):
            self.frequency+=2
            self.positionSlider.setValue(self.frequency)
            self.title.setText("FM " + str(self.frequency / 10.0))
            changechannel(self.frequency)
        else:
            pass
    def prev(self):
        if(self.frequency>880):
            self.frequency-=2
            self.positionSlider.setValue(self.frequency)
            self.title.setText("FM " + str(self.frequency / 10.0))
            print(self.frequency)
            changechannel(self.frequency)
        else:
            pass
    def play(self):
        if self.playing==True:
            self.playButton.setIcon(
                QIcon('/home/pi/music2/img/play_circle.png'))
            self.playButton.setIconSize(QSize(30, 30))
            self.playing=False
            setvolume(0)
        else:
            self.playButton.setIcon(
                QIcon('/home/pi/music2/img/pause_circle.png'))
            a=self.vol/10
            #print(a)
            setvolume(a)
            self.playing = True
    def mute(self, state):
        if self.mutestate==False:
            self.muteButton.setIcon(
                QIcon('/home/pi/music2/img/mute.png'))
            self.mutestate = True
            self.Gvol = self.vol
            self.volSlider.setValue(0)
            self.setVolume(0)
        else:
            self.muteButton.setIcon(
                QIcon('/home/pi/music2/img/unmute.png'))
            self.mutestate = False
            self.vol = self.Gvol
            self.volSlider.setValue(self.vol)
            self.setVolume(self.vol)
    def homeclick(self):
        self.hide()
    def pageswitch(self):
        if self.listMode == False:
            self.listFrame.show()
            self.listMode=True
            self.pageButton.setIcon(QIcon('/home/pi/music2/img/tv1.png'))
            self.pageButton.setIconSize(QSize(30, 25))
            self.coverImage.setVisible(False)
        else:
            self.listFrame.hide()
            self.pageButton.setIcon(QIcon('/home/pi/music2/img/list.png'))
            self.pageButton.setIconSize(QSize(30, 30))
            self.listMode = False
            self.coverImage.setVisible(True)
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Radio = Ui_Radio()
    Radio.setFixedSize(QSize(800, 480))
    Radio.show()
    Radio.move(0,0)
    sys.exit(app.exec_())
