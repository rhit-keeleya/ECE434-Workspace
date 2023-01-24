#!/usr/bin/env python3


"""
Blynk is a platform with iOS and Android apps to control
Arduino, Raspberry Pi and the likes over the Internet.
You can easily build graphic interfaces for all your
projects by simply dragging and dropping widgets.
  Downloads, docs, tutorials: http://www.blynk.cc
  Sketch generator:           http://examples.blynk.cc
  Blynk community:            http://community.blynk.cc
  Social networks:            http://www.fb.com/blynkapp
                              http://twitter.com/blynk_app
"""

import BlynkLib
import time
import os
import smbus
import time
import gpiod

BLYNK_AUTH = 'JZoUYgzo3hN9RtvxiRNXhrc7bvHMQrNn'

# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)
timestamp = time.time_ns()
delay = 3*10**7   # delay in ns

## etch-a-sketch stuff
size = 8 # <- 8x8 matrix
xCor = 0
yCor = 7

## matrix stuff
data = [0x00]*16
bus = smbus.SMBus(2)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70
color = 0 # 0-> green, 1-> red, 2-> orange

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
map()
draw()

@blynk.on("V0")
def blynk_handle_vpins(value):
    #erase button
    erase()
    map()
    draw()

@blynk.on("V1")
def blynk_handle_vpins(value):
    # joystick
    global xCor
    global yCor
    global timestamp
    if(time.time_ns()-timestamp>delay):
        # slow down the controls slightly
        if(int(value[0])>200):
            xCor = min(size-1,xCor+1)
        if(int(value[0])<50):
            xCor = max(0,xCor-1)
        if(int(value[1])>200):
            yCor = min(size-1,yCor+1)
        if(int(value[1])<50):
            yCor = max(0,yCor-1)
        map()
        draw()
    timestamp = time.time_ns()

@blynk.on("V2")
def blynk_handle_vpins(value):
    global color
    color = int(value[0])
    map()
    draw()

@blynk.on("connected")
def blynk_connected():
    # initial connection, synchronize (update color)
    blynk.sync_virtual(1,2,3)

while True:
    blynk.run()
    blink()