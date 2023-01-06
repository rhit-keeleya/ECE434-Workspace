#!/usr/bin/env bash
## temp.sh	Abel Keeley	12/16/22
## Gets temperature from T101 sensors on addresses 0x48, 0x49 on I2C bus 2

# get temps
T1=`i2cget -y 2 0x48 0`
T2=`i2cget -y 2 0x49 0`
# format hex
T1=`echo $T1 | cut -d 'x' -f 2`
T2=`echo $T2 | cut -d 'x' -f 2`
# convert to decimal
T1=`echo "obase=10; ibase=16; $T1" | bc`
T2=`echo "obase=10; ibase=16; $T2" | bc`
# convert from C to Fahrenheit
let T1=T1*9/5+32 T2=T2*9/5+32

echo "Temperature from sensor 0x48: $T1"
echo "Temperature from sensor 0x49: $T2"
