# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Radio.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
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
    print "Trying Station ", float(float(getchannel())/float(10))
    read_registers()
    valuesfbl = reg[STATUSRSSI] & (1<<13)
    reg[POWERCFG] &= ~(1<<8)
    write_registers()
    return

init() #init stuff

changechannel(890) #89.0 
setvolume(7)