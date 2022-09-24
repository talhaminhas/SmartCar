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

class PhoneWindow(QMainWindow):
    def __init__(self, parent=None):
        super(PhoneWindow, self).__init__(parent)
        self.setWindowTitle("Dialer")

        self.listFrame=QFrame()
        self.title=QLabel()

        self.contactlist = QListWidget()
        self.HomeButton = QPushButton()
        self.textbox = QLineEdit(self)

        #Dialer Buttons
        self.one = QPushButton()
        self.two = QPushButton()
        self.three = QPushButton()
        self.four = QPushButton()
        self.five = QPushButton()
        self.six = QPushButton()
        self.seven = QPushButton()
        self.eight = QPushButton()
        self.nine = QPushButton()
        self.star = QPushButton()
        self.zero = QPushButton()
        self.hash = QPushButton()
        self.dial = QPushButton()
        self.hangup = QPushButton()
        self.clear = QPushButton()

        self.guiBuilder()
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)
	wid.setStyleSheet("background-image: url(/home/pi/music2/img/back1.jpeg); background-attachment: fixed")
        
        

        h1 = QHBoxLayout()
        h1.setContentsMargins(0, 0, 0, 0)
        h1.addWidget(self.one)
        h1.addWidget(self.two)
        h1.addWidget(self.three)
        h2 = QHBoxLayout()
        h2.setContentsMargins(0, 0, 0, 0)
        h2.addWidget(self.four)
        h2.addWidget(self.five)
        h2.addWidget(self.six)
        h3 = QHBoxLayout()
        h3.setContentsMargins(0, 0, 0, 0)
        h3.addWidget(self.seven)
        h3.addWidget(self.eight)
        h3.addWidget(self.nine)
        h4 = QHBoxLayout()
        h4.setContentsMargins(0, 0, 0, 0)
        h4.addWidget(self.star)
        h4.addWidget(self.zero)
        h4.addWidget(self.hash)
        h5 = QHBoxLayout()
        h5.setContentsMargins(0, 0, 0, 0)
        h5.addWidget(self.hangup)
        
        
        h5.addWidget(self.clear)
        h5.addWidget(self.dial)


        v1 = QVBoxLayout()
        v1.addWidget(self.textbox)
        v1.addLayout(h1)
        v1.addLayout(h2)
        v1.addLayout(h3)
        v1.addLayout(h4)
        v1.addLayout(h5)


        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(5, 5, 5, 5)
        
        topLayout.addWidget(self.title)
        topLayout.addWidget(self.HomeButton)


        listLayout = QHBoxLayout()
        listLayout.addWidget(self.contactlist)
        listLayout.addLayout(v1)
        self.listFrame.setLayout(listLayout)
        self.listFrame.setFixedSize(QSize(800,300))
        #self.listFrame.hide()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(topLayout)
        layout.addWidget(self.listFrame)

        # Set widget to contain window contents
        wid.setLayout(layout)

    def guiBuilder(self):
        p = self.palette()
        self.palette().setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        #self.setStyleSheet("background-color:#000000")

        font1 = QFont("Bahnschrift SemiBold", 20)
        self.title.setFixedSize(780, 40)
        self.title.setStyleSheet("color:#F4F8F7")
        self.title.setFont(font1)
        self.title.setText("Phone Book")
        self.title.setAlignment(Qt.AlignHCenter)

        font2 = QFont("Bahnschrift SemiBold", 13)
        #self.contactlist.setStyleSheet("color:#F4F8F7")
        self.contactlist.setVisible(True)
        self.contactlist.setFixedSize(430,270)
        self.contactlist.setFont(font2)
        self.contactlist.clicked.connect(self.contactClick)
        self.contactlist.addItem("Mian Saram\n03459268135\n")
        self.contactlist.addItem("Deepak Kumar\n03459268134\n")
        self.contactlist.addItem("Talha Minhas\n03155799969\n")
        self.contactlist.addItem("Imran Gul\n03456243582\n")
        self.contactlist.addItem("Kanwar Danish\n03459387243\n")
        self.contactlist.addItem("Aizaz Cheema\n03452735463\n")
        self.contactlist.addItem("Faizan Malik\n03450376532\n")
        #self.contactlist.clicked.connect(self.listclicked)
        
        self.textbox.setFixedSize(300,40)
        self.textbox.setFont(font1)
        self.textbox.setAlignment(Qt.AlignHCenter)
        self.textbox.setPlaceholderText("Enter Number")
        
        self.HomeButton.setIcon(QIcon('/home/pi/music2/img/home.png'))
        self.HomeButton.setIconSize(QSize(25, 25))
        self.HomeButton.clicked.connect(self.homeclick)

        self.one.setIcon(QIcon("/home/pi/music2/img/1.png"))
        self.one.setIconSize(QSize(30, 30))
        self.one.clicked.connect(self.f1)
        self.one.setText("")
        self.two.setIcon(QIcon('/home/pi/music2/img/2.png'))
        self.two.setIconSize(QSize(30, 30))
        self.two.clicked.connect(self.f2)
        self.three.setIcon(QIcon('/home/pi/music2/img/3.png'))
        self.three.setIconSize(QSize(30, 30))
        self.three.clicked.connect(self.f3)
        self.four.setIcon(QIcon('/home/pi/music2/img/4.png'))
        self.four.setIconSize(QSize(30, 30))
        self.four.clicked.connect(self.f4)
        self.five.setIcon(QIcon('/home/pi/music2/img/5.png'))
        self.five.setIconSize(QSize(30, 30))
        self.five.clicked.connect(self.f5)
        self.six.setIcon(QIcon('/home/pi/music2/img/6.png'))
        self.six.setIconSize(QSize(30, 30))
        self.six.clicked.connect(self.f6)
        self.seven.setIcon(QIcon('/home/pi/music2/img/7.png'))
        self.seven.setIconSize(QSize(30, 30))
        self.seven.clicked.connect(self.f7)
        self.eight.setIcon(QIcon('/home/pi/music2/img/8.png'))
        self.eight.setIconSize(QSize(30, 30))
        self.eight.clicked.connect(self.f8)
        self.nine.setIcon(QIcon('/home/pi/music2/img/9.png'))
        self.nine.setIconSize(QSize(30, 30))
        self.nine.clicked.connect(self.f9)
        self.star.setIcon(QIcon('/home/pi/music2/img/star.png'))
        self.star.setIconSize(QSize(30, 50))
        self.star.clicked.connect(self.fstar)
        self.zero.setIcon(QIcon('/home/pi/music2/img/0.png'))
        self.zero.setIconSize(QSize(30, 30))
        self.zero.clicked.connect(self.f0)
        self.hash.setIcon(QIcon('/home/pi/music2/img/hash.png'))
        self.hash.setIconSize(QSize(30, 50))
        self.hash.clicked.connect(self.fhash)
        self.dial.setIcon(QIcon('/home/pi/music2/img/dial.png'))
        self.dial.setIconSize(QSize(30, 30))
        self.dial.clicked.connect(self.fdial)
        self.hangup.setIcon(QIcon('/home/pi/music2/img/hangup.png'))
        self.hangup.setIconSize(QSize(35, 35))
        self.hangup.clicked.connect(self.fhangup)
        self.clear.setIcon(QIcon('/home/pi/music2/img/clear.png'))
        self.clear.setIconSize(QSize(30, 50))
        self.clear.clicked.connect(self.fclear)
        
    def f1(self):
        self.textbox.setText(self.textbox.text()+"1")
    def f2(self):
        self.textbox.setText(self.textbox.text()+"2")
    def f3(self):
        self.textbox.setText(self.textbox.text()+"3")
    def f4(self):
        self.textbox.setText(self.textbox.text()+"4")
    def f5(self):
        self.textbox.setText(self.textbox.text()+"5")
    def f6(self):
        self.textbox.setText(self.textbox.text()+"6")
    def f7(self):
        self.textbox.setText(self.textbox.text()+"7")
    def f8(self):
        self.textbox.setText(self.textbox.text()+"8")
    def f9(self):
        self.textbox.setText(self.textbox.text()+"9")
    def f0(self):
        self.textbox.setText(self.textbox.text()+"0")
    def fstar(self):
        self.textbox.setText(self.textbox.text()+"*")
    def fhash(self):
        self.textbox.setText(self.textbox.text()+"#")
    def fdial(self):
        number=self.textbox.text()
	#os.system("cd ..")
	os.system(" python /home/pi/ofono-1.21/test/dial-number "+number)
    def fhangup(self):
        os.system("/home/pi/ofono-1.21/test/hangup-all")
    def fclear(self):
        self.textbox.setText("")
    def contactClick(self):
        word  = self.contactlist.currentItem().text().split('\n')
        self.textbox.setText(word[1])
    def homeclick(self):
        self.hide()    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = PhoneWindow()
    player.setFixedSize(QSize(800,480))
    player.show()
    sys.exit(app.exec_())

    