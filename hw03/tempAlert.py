#!/usr/bin/env python3

# tempAler.py   Abel Keeley 12/16/22
# Waits for an interupt on P9_11, P9_13 and then gets temperature from T101 sensors on i2cbus 2, addresses 0x48, 0x49

import smbus
import time
import gpiod

address1 = 0x49
address2 = 0x48
tempReg = 0
configReg = 1
TlReg = 2
ThReg = 3
i2cbus = 2

temp1 = 0
temp2 = 0

def setup():
    global i2cbus
    i2cbus = smbus.SMBus(i2cbus)
    setupThTl(address1,77,77)
    setupThTl(address2,74,74)
    setConfig(address1)
    setConfig(address2)
    return setupAlert("0",[30,31])

def setupAlert(chip, offset):
    # Sets up 
    alertChip = gpiod.Chip(chip)
    alertLines = alertChip.get_lines(offset)
    alertLines.request(consumer="tempAlert", type=gpiod.LINE_REQ_EV_FALLING_EDGE)
    return alertLines

def getTemp(addr):
    # fetch temp in Celsius
    temp = i2cbus.read_byte_data(addr,0)
    # convert to Fahrenheit
    return temp * 9/5 + 32

def setConfig(addr):
    # setup alerts
    config = 4
    i2cbus.write_byte_data(addr,configReg,config)


def getConfig():
    # prints out contents of config register in binary - useful for debugging!
    config = i2cbus.read_byte_data(address1,configReg)
    config = int(config)
    result = ""
    for i in range(8):
        if (config>=2**(7-i) and config%(2**(7-i))==0):
            result = result + "1"
            config -= 2**(7-i)
        else:
            result = result + "0"
    print("Config: "+result)

def setupThTl(addr, Th, Tl):
    # assumes Th/Tl are above 32 degrees F
    i2cbus.write_byte_data(addr,TlReg, int((Tl-32) * 5/9))
    i2cbus.write_byte_data(addr,ThReg, int((Th-32) * 5/9))


print("Fetching temperature from T101 sensors")

alerts = setup()

while(1):
    # print("Sensor1 temp: "+str(getTemp(address1))+"F, Sensor2 temp: "+str(getTemp(address2))+"F",end='\r')
    alertEvents = alerts.event_wait(nsec=10**7)
    if alertEvents:
        for line in alertEvents:
            event = line.event_read()
            if(event.source.offset()==30):
                print("EVENT! Sensor 1 temp is:" +str(getTemp(address1))+"F")
            if(event.source.offset()==31):
                print("EVENT! Sensor 2 temp is:" +str(getTemp(address2))+"F")