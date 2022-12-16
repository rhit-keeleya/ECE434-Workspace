#!/usr/bin/env python3

# temp.py   Abel Keeley 12/16/22
# Gets temperature from T101 sensors on i2cbus 2, addresses 0x48, 0x49

import smbus
import time

address1 = 0x48
address2 = 0x49
i2cbus = 2
temp1 = 0
temp2 = 0

def setup():
    global i2cbus
    i2cbus = smbus.SMBus(i2cbus)

def getTemp(addr):
    # fetch temp in Celsius
    temp = i2cbus.read_byte_data(addr,0)
    # convert to Fahrenheit
    return temp * 9/5 + 32

print("Fetching temperature from T101 sensors")

setup()

while(1):
    print("Sensor1 temp: "+str(getTemp(address1))+"F, Sensor2 temp: "+str(getTemp(address2))+"F",end='\r')
    time.sleep(0.1)