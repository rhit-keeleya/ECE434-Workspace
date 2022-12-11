#!/usr/bin/env python3
# //////////////////////////////////////
# 	getsetEvent.py
#   Like getset.py but uses events.
#   Get the value of P8_16 and write it to P9_14. 
#     P8_16 is line 14 on chip 1.  P9_14 is line 18 of chip 1.
# 	Wiring:	Attach a switch to P8_16 and 3.3V and an LED to P9_14.
# 	Setup:	sudo apt uupdate; sudo apt install libgpiod-dev
#           Run: gpioinfo | grep -i -e chip -e P9_14 to find chip and line numbers
# 	See:	https://github.com/starnight/libgpiod-example/blob/master/libgpiod-led/main.c
# //////////////////////////////////////
# Based on https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/tree/bindings/python/examples

import gpiod
import sys

CONSUMER='getset'

setoffsets=[2,3,5,4]
getoffsets=[23,26,27,22]


def print_event(event):
    if event.type == gpiod.LineEvent.RISING_EDGE:
        evstr = ' RISING EDGE'
    elif event.type == gpiod.LineEvent.FALLING_EDGE:
        evstr = 'FALLING EDGE'
    else:
        raise TypeError('Invalid event type')

    print('event: {} offset: {} timestamp: [{}.{}]'.format(evstr,
                                                           event.source.offset(),
                                                      event.sec, event.nsec))

getChip = gpiod.Chip("0")
getlines = getChip.get_lines(getoffsets)
getlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)

setChip = gpiod.Chip("2")
setlines = setChip.get_lines(setoffsets)
setlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)

print("Hit ^C to stop")

while True:
    ev_lines = getlines.event_wait(sec=1)
    if ev_lines:
        for line in ev_lines:
            event = line.event_read()
            print_event(event)
    vals = getlines.get_values()
    setlines.set_values(vals)