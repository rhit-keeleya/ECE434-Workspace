#!/usr/bin/env python3

# online-etch-a-sketch.py	Abel Keeley	1/8/23
# Does what it says on the box...
# Run with "./online-etch-a-sketch.py" and go to port 8081

import os
import smbus

from flask import Flask, render_template
app = Flask(__name__)

grid = [["White"]*8 for _ in range(8)]
color = "Green"
x = 0
y = 0

## matrix stuff
data = [0x00]*16
bus = smbus.SMBus(2)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70

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
	xCor = x
	yCor = (7-y)
	if(color == "Green"):
		colorID = 0
	if(color == "Red"):
		colorID = 1
	if(color == "Orange"):
		colorID = 2
	# wipe current position
	data[xCor*2+1] = (~2**yCor & data[xCor*2+1])
	data[xCor*2] = (~2**yCor & data[xCor*2])
	# write new data to current position
	data[xCor*2+colorID%2] = (2**yCor|data[xCor*2+colorID%2])
	if(colorID==2):
		data[xCor*2+1] = (2**yCor|data[xCor*2+1])

setupMatrix()

def move(direction):
	global x
	global y
	if(direction == "up"):
		y = max(0,y-1)
	elif(direction == "down"):
		y = min(7,y+1)
	elif(direction == "left"):
		x = max(0,x-1)
	elif(direction == "right"):
		x = min(7,x+1)

def updateGrid():
	global grid
	grid[y][x] = color

def getGridDict():
	result = {}
	for i in range(8):
		for j in range(8):
			key = "color"+str(i*8+j)
			value = grid[i][j]
			result[key]=value
	return result

def erase():
	global grid
	global data
	grid = [["White"]*8 for _ in range(8)]
	data = [0x00]*16

@app.route("/")
def index():
	# update
	updateGrid()
	map()
	draw()
	# Show game status
	templateData = getGridDict()
	return render_template('etch-a-sketch.html', **templateData)

@app.route("/<command>/<parameter>")
def action(command, parameter):
	global color
	if (command == "color"):
		color = parameter
	
	if (command == "move"):
		move(parameter)

	if (command == "control"):
		if (parameter == "erase"):
			erase()
			print(data)

	# update
	updateGrid()
	map()
	draw()
	# Show updated game status
	templateData = getGridDict()
	return render_template('etch-a-sketch.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8081, debug=True)