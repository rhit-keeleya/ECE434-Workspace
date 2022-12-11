#!/usr/bin/env python3

from curses import wrapper
import curses
import math
import random
import gpiod
import time

xCor = 0
yCor = 0
stdscr = 0
getLines = [23,26,27,22]
getChip = "0"
lines = ""

def drawPos():
	global xCor
	global yCor

	rows,cols = stdscr.getmaxyx()

	#check that we are in bounds
	xCor = max(1,min(cols-2,xCor))
	yCor = max(1,min(rows-2,yCor))
	stdscr.addch(yCor,xCor,'▓')
	stdscr.move(yCor,xCor)
	stdscr.refresh()

def erase():
	stdscr.clear()
	stdscr.border()
	stdscr.refresh()
	
def wordWrap(string):
	y,x = stdscr.getmaxyx()

	#make sure we stay in bounds
	curY,curX = stdscr.getyx()
	curY = max(1,min(y-2,curY))
	curX = 1
	stdscr.move(curY,curX)

	if (len(string) < (x-2)):
		stdscr.addstr(string)
	else:
		words = string.split()
		for word in words:
			curX += len(word)+1
			if (curX <= (x-1)):
				stdscr.addstr(word + " ")
			else:
				if(curY <= y-2):
					curX = 1
					curY += 1
					stdscr.move(curY,curX)
					curX += len(word)+1
					stdscr.addstr(word + " ")

	curX = 1
	curY += 1
	stdscr.move(curY,curX)
	stdscr.refresh()

def setupButtons():
	global lines
	Chip = gpiod.Chip(getChip)
	lines = Chip.get_lines(getLines)
	lines.request(consumer="Blink", type=gpiod.LINE_REQ_EV_RISING_EDGE, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)

def getButton():
	vals = [0,0,0,0]
	ev_lines = lines.event_wait(sec=1)
	if ev_lines:
		for line in ev_lines:
			line.event_read()
		vals = lines.get_values()

	numButtons = 0

	for i in range(len(vals)):
		numButtons += vals[i]
	
	if(numButtons == 4):
		return "QUIT"
	elif(numButtons == 2):
		return "ERASE"
	else:
		if (vals[0]):
			return "LEFT"
		elif (vals[1]):
			return "UP"
		elif (vals[2]):
			return "DOWN"
		elif (vals[3]):
			return "RIGHT"
	return "NONE"
	
def input():
	#captures inputs
	global xCor
	global yCor
	key = getButton()
	
	if (key=="UP"):
		yCor -=1
	elif (key=="DOWN"):
		yCor +=1
	elif (key=="RIGHT"):
		xCor +=1
	elif (key=="LEFT"):
		xCor -=1
	elif (key=="QUIT"):
		raise Exception("Quit")
	elif (key=="ERASE"):
		erase()

	drawPos()

def background():
	#fills the background with some random noise
	global xCor
	global yCor

	y,x = stdscr.getmaxyx()

	for i in range(y-2):
		row = ""
		for j in range(x-2):
			if(bool(random.getrandbits(1))):
				row = row + "▓"
			else:
				row = row + " "
		wordWrap(row[0:-1])
	stdscr.move(1,1)

def tutorial():
	global xCor
	global yCor

	#clear the screen
	erase()
	background()

	# use word wrap
	wordWrap("Welcome to my etch-a-sketch program! - Abel")
	wordWrap("You can use the push buttons to interact with program.")
	wordWrap("Try it now! Press any key to continue...")

	while(getButton() == "NONE"):
		xCor = 0
	
	#erase, draw, write
	erase()
	background()

	wordWrap("Press a single button to move the pen, and press two buttons to erase.")
	wordWrap("Press all four buttons to quit.")
	wordWrap("Note that the display will resize with your terminal window after erasing.")
	wordWrap("Erase this screen when you are ready to get started.")

	while(getButton() != "ERASE"):
		xCor = 0

def main(scr):
	global stdscr
	stdscr = scr
	setupButtons()
	tutorial()
	while True:
		input()

try:
	wrapper(main)
except:
	print('Quitting...')