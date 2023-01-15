#!/usr/bin/env bash
## setup.sh	Abel Keeley	12/16/22
## Sets up an ADXL345 on I2C bus 2, address 0x53
ADDR=0x53

cd /sys/class/i2c-adapter/i2c-2/
# remove any existing devices on the address
echo Attempting to remove existing devices on $ADDR
echo $ADDR > delete_device
# add the new device
echo Adding adxl345 on $ADDR
echo adxl345 $ADDR > new_device