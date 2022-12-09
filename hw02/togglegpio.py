#!/usr/bin/env python

import time
import sys

delay = float(sys.argv[2])
GPIOpin = sys.argv[1]
path = "/sys/class/gpio/gpio"+GPIOpin+"/value"

value = 1

try:
	while (True):
		gpio = open(path,"w")
		gpio.write(str(value))
		gpio.close()
		value = value ^ 1
		time.sleep(delay/1000)
except:
	print("\nCleaning up...")
	gpio = open(path,"w")
	gpio.write("0")
	gpio.close()
