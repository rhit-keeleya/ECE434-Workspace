#!/usr/bin/env python3

from curses import wrapper
import curses
import math

xCor = 0
yCor = 0

def drawPos(stdscr):
	global xCor
	global yCor

	rows,cols = stdscr.getmaxyx()

	#check that we are in bounds
	xCor = max(1,min(cols-2,xCor))
	yCor = max(1,min(rows-2,yCor))
	stdscr.addch(yCor,xCor,'▓')
	stdscr.refresh()


def erase(stdscr):
	stdscr.clear()
	stdscr.border()
	stdscr.refresh()
	


def input(stdscr):
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
		erase(stdscr)
	drawPos(stdscr)

def instructions(stdscr):
	# Clear screen
	stdscr.clear()
	curses.curs_set(0)
	# Print instructions
	stdscr.addstr("Welcome to my etch-a-sketch program! - Abel\n")
	stdscr.addstr("You can use your keyboard to interact with program.\n")
	stdscr.addstr("Try it now! Press any key to continue...\n")
	stdscr.refresh()
	stdscr.getkey()

	stdscr.clear()
	stdscr.addstr("Use arrow keys to move the pen, and press space to erase the screen.\n")
	stdscr.addstr("Press q to quit.\n")
	stdscr.addstr("Note that the display will resize with your terminal window after erasing.\n")
	stdscr.addstr("Erase this screen when you are ready to get started.\n")
	stdscr.refresh()

	while True:
		input(stdscr)

def main(stdscr):
	instructions(stdscr)

try:
	wrapper(main)
except:
	print('Quitting...')