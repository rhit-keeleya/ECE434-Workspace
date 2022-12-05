#!/usr/bin/env python3

from curses import wrapper
import curses
import math
import random

xCor = 0
yCor = 0
stdscr = 0

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


def input():
	#captures inputs
	global xCor
	global yCor
	key = stdscr.getkey()

	if (key=="KEY_UP"):
		yCor -=1
	elif (key=="KEY_DOWN"):
		yCor +=1
	elif (key=="KEY_RIGHT"):
		xCor +=1
	elif (key=="KEY_LEFT"):
		xCor -=1
	elif (key=="q"):
		raise Exception("Quit")
	elif (key==" "):
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
	wordWrap("You can use your keyboard to interact with program.")
	wordWrap("Try it now! Press any key to continue...")
	stdscr.getkey()

	#erase, draw, write
	erase()
	background()

	wordWrap("Use arrow keys to move the pen, and press space to erase the screen.")
	wordWrap("Press q to quit.")
	wordWrap("Note that the display will resize with your terminal window after erasing.")
	wordWrap("Erase this screen when you are ready to get started.")

def main(scr):
	global stdscr
	stdscr = scr
	#instructions()
	tutorial()
	while True:
		input()

try:
	wrapper(main)
except:
	print('Quitting...')