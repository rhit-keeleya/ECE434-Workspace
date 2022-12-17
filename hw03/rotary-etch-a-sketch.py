#!/usr/bin/env python3

import os
import smbus
import time
import gpiod

## etch-a-sketch stuff
size = 8 # <- 8x8 matrix
xCor = 0
yCor = 0
xCount = 0
yCount = 0

## matrix stuff
data = [0x00]*16
bus = smbus.SMBus(2)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70
color = 0 # 0-> green, 1-> red, 2-> orange

## T101 stuff
eraseAddress = 0x49
colorAddress = 0x48
tempReg = 0
configReg = 1
TlReg = 2
ThReg = 3
eventTemp = 70	# temp in degrees F

def setupTMP():
	global eventTemp
	setConfig(eraseAddress)
	setConfig(colorAddress)
	setupThTl(eraseAddress,eventTemp)
	eventTemp = setupThTl(colorAddress,eventTemp)
	return setupAlert("0",[30,31])

def setConfig(addr):
    # setup alerts, and 10-bit resolution
    config = 0b00100100
    bus.write_byte_data(addr,configReg,config)

def setupThTl(addr, temp):
    # assumes temp is above 32 degrees F
	temp = ((float(temp)-32)*5/9) # convert to C
	temp = int(temp*(1/(0.25))) # convert to 10-bit resolution
	block = [0]*2
	block[0] = temp>>2 # first byte
	block[1] = temp<<6 & 0xFF # second byte
	bus.write_i2c_block_data(addr,TlReg, block)
	bus.write_i2c_block_data(addr,ThReg, block)
	return float(block[0]<<2|block[1]>>6)*0.25*9/5+32 # return the actual set temp in Fahrenheit

def setupAlert(chip, offset):
    # Sets up interrupt for P9_11, P9_13
    alertChip = gpiod.Chip(chip)
    alertLines = alertChip.get_lines(offset)
    alertLines.request(consumer="tempAlert", type=gpiod.LINE_REQ_EV_FALLING_EDGE)
    return alertLines

def getTemp(addr):
	# fetch temp
	temp = bus.read_i2c_block_data(addr,0)
	temp = float((temp[0]<<2)+(temp[1]>>6)) # get 10-bit temp
	temp = temp * 0.25 # convert temp to C
	# convert to Fahrenheit
	return temp * 9/5 + 32

def setupEncoders():
	# configure pins for eqep 1
	os.system("config-pin P8_11 eqep > /dev/null; config-pin P8_12 eqep > /dev/null")
	# configure pins for eqep 2
	os.system("config-pin P8_33 eqep > /dev/null; config-pin P8_35 eqep > /dev/null")
	ceiling = size * 1048576 - 1 # make ceiling big enough we don't have to worry about overflow/wraparound
	# setup eqep 1 for rotary encoder
	os.system("cd /dev/bone/counter/1/count0; echo 1 > enable; echo "+str(ceiling)+" > ceiling")
	# setup eqep 2 for rotary encoder
	os.system("cd /dev/bone/counter/2/count0; echo 1 > enable; echo "+str(ceiling)+" > ceiling")

def getEncoders():
	# checks each encoders count, updates x, yEncoder, returns true if either encoder has changed
	global xCor
	global yCor
	global xCount
	global yCount
	xFile = open('/dev/bone/counter/1/count0/count',"r")
	x = int(int(xFile.read())/4) # normalize counts
	xFile.close()
	yFile = open("/dev/bone/counter/2/count0/count","r")
	y = int(int(yFile.read())/4)
	yFile.close()

	# figure out if count has increased or decreased since last reading
	if(((xCount + 512 - x) % 1024 - 512)>0):
		xCor=min(xCor+1,size-1)
		xCount = x
		return True
	if(((xCount + 512 - x) % 1024 - 512)<0):
		xCor=max(0,xCor-1)
		xCount = x
		return True
	if(((yCount + 512 - y) % 1024 - 512)>0):
		yCor=min(size-1,yCor+1)
		yCount = y
		return True
	if(((yCount + 512 - y) % 1024 - 512)<0):
		yCor=max(yCor-1,0)
		yCount = y
		return True

def setupMatrix():
	# Much of the setup is taken from the example code provided
	bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
	bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
	bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

def draw():
	# update the matrix
	bus.write_i2c_block_data(matrix, 0, data)

def map():
	# maps the x,y coordinates to the data variable
	global data
	data[xCor*2+color%2] = (2**yCor|data[xCor*2+color%2])
	if(color==2):
		data[xCor*2+1] = (2**yCor|data[xCor*2+1])

def blink():
	# blinks the led at the pen's position
	global data
	# turn off the led at the current position
	data[xCor*2+color%2] = (~2**yCor & data[xCor*2+color%2])
	if(color==2):
		data[xCor*2+1] = (~ 2**yCor & data[xCor*2+1])
	draw()
	# wait a short while
	time.sleep(0.01)
	# turn it back on
	map()
	draw()
	
def erase():
	global data
	data = [0x00]*16 # reset data
	draw() # update screen

setupMatrix()
setupEncoders()
alerts = setupTMP()
# need to get encoders twice and reset coordinates to avoid any initial offset
getEncoders()
getEncoders()
xCor = 0
yCor = 0
map()
draw()

while(True):
	if(getEncoders()):
		map()
		draw()
	alertEvents = alerts.event_wait(nsec=10**7)
	if alertEvents:
		for line in alertEvents:
			event = line.event_read()
			if(event.source.offset()==30):
				# erase
				erase()
			if(event.source.offset()==31):
				# change color
				color = (color+1)%3
	blink()
	print("Trigger temp: "+str(eventTemp)+"F, Color Sensor: "+
	str(getTemp(colorAddress)).ljust(5,'0')+"F, Erase sensor: "+
	str(getTemp(eraseAddress)).ljust(5,'0')+"F",end='\r')