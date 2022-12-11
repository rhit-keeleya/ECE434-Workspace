#!/usr/bin/env python

import gpiod
import time
import signal

ledPins = [66,67,69,68]
ledLines = []
switchPins = [23,26,27,22]
switchLines = []
chips = []

def handler(signum, frame):
    print("\nClosing chips...")
    for i in range(len(chips)):
        chips[i].close()
    exit(1)

signal.signal(signal.SIGINT, handler)

for pin in ledPins:
    chipStr = "gpiochip"+str(int(pin/32))
    lineNum = pin%32
    chip = gpiod.Chip(chipStr)
    line = chip.get_line(lineNum)
    line.request(consumer="Blink", type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
    ledLines.append(line)
    chips.append(chip)

for pin in switchPins:
    chipStr = "gpiochip"+str(int(pin/32))
    lineNum = pin%32
    chip = gpiod.Chip(chipStr)
    line = chip.get_line(lineNum)
    line.request(consumer="Blink", type=gpiod.LINE_REQ_DIR_IN)#, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)
    switchLines.append(line)
    chips.append(chip)

while True:
    for i in range(len(ledPins)):
        ledLines[i].set_value(switchLines[i].get_value())
    time.sleep(0.05)