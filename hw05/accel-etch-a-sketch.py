#!/usr/bin/env python3

import os
import smbus
import time
import gpiod

## etch-a-sketch stuff
size = 8 # <- 8x8 matrix
xCor = 0
yCor = 7

## matrix stuff
data = [0x00]*16
bus = smbus.SMBus(2)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70
color = 0 # 0-> green, 1-> red, 2-> orange

## accelerometer stuff
path = "/sys/class/i2c-adapter/i2c-2/2-0053/iio:device1"
deadzone = 20
wait = 0.4 # <- delay between polling
zBuffer = []
length = 3
index = 0
cThreshold = 300
eThreshold = 500

def setupAccel():
	global zBuffer
	setup = os.path.exists(path)
	if(not setup):
		# run setup script
		print("Need sudo permission to setup the adxl345 device...")
		os.system("sudo ./setup.sh")
	# setup zBuffer w/ initial values
	zFile = open('/sys/class/i2c-adapter/i2c-2/2-0053/iio:device1/in_accel_z_raw',"r")
	z = int(zFile.read())
	zFile.close()
	zBuffer = [z]*length

def calibrate(num):
	# establish deadzone
	if(num>deadzone):
		return 1
	if(num<-deadzone):
		return -1
	return 0

def getAccel():
	global xCor
	global yCor

	yFile = open('/sys/class/i2c-adapter/i2c-2/2-0053/iio:device1/in_accel_y_raw',"r")
	y = int(yFile.read())
	yFile.close()

	xFile = open('/sys/class/i2c-adapter/i2c-2/2-0053/iio:device1/in_accel_x_raw',"r")
	x = int(xFile.read())
	xFile.close()

	yCor = min(size-1,max(0,yCor + calibrate(y)))
	xCor = min(size-1,max(0,xCor + calibrate(x)))

def updateBuffer():
	global zBuffer
	global index
	global color
	zFile = open('/sys/class/i2c-adapter/i2c-2/2-0053/iio:device1/in_accel_z_raw',"r")
	z = int(zFile.read())
	zFile.close()

	# start filling a circular buffer of z values
	index = (index+1)%length
	zBuffer[index] = z

	# detect if z changing rapidly
	delta = abs(max(zBuffer)-min(zBuffer))

	if(delta>eThreshold):
		erase()
	elif(delta>cThreshold):
		color = (color+1)%3

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
	# wipe current position
	data[xCor*2+1] = (~2**yCor & data[xCor*2+1])
	data[xCor*2] = (~2**yCor & data[xCor*2])
	# write new data to current position
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
	time.sleep(0.02)

def erase():
	global data
	data = [0x00]*16 # reset data
	draw() # update screen

setupMatrix()
erase()
setupAccel()
print("Instructions: tilt breadboard to move, shake gently to change colors and vigorously to erase.")

# main loop
while(True):
	# update coordinates
	getAccel()
	# update matrix
	map()
	draw()
	# blink current position and update buffer for <wait> amount of time
	start = time.time()
	while(time.time()<start+wait):
		updateBuffer()
		blink()