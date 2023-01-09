#!/usr/bin/env bash
# temp.sh	Abel Keeley	1/8/23

# setup device
cd /sys/class/i2c-adapter/i2c-2/2-0048/hwmon/hwmon0

# get temp in degrees C
TEMPC=`cat temp1_input`
REMAINC=$(($TEMPC%1000))
TEMPC=$(($TEMPC/1000))

# convert to degrees F
TEMPF=$(($TEMPC*9/5+32))
REMAINF=$((REMAINC*9/5))
CARRYF=$((REMAINF/1000))
REMAINF=$((REMAINF%1000))

#print it out:
echo Temp: $(($TEMPF+$CARRYF)).$REMAINF F, $TEMPC.$REMAINC C
