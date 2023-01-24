#!/usr/bin/env bash
## temp.sh	Abel Keeley	1/23/23
## Reads hwmon0-3, assumes that all three are temperature sensors reporting millidegrees centigrade

# function that takes millidegrees centigrade, converts to F, and prints
print_F() {
    TEMPC=$1
    #convert to F
    REMAINC=$(($TEMPC%1000))
    TEMPC=$(($TEMPC/1000))
    TEMPF=$(($TEMPC*9/5+32))
    REMAINF=$((REMAINC*9/5))
    CARRYF=$((REMAINF/1000))
    REMAINF=$((REMAINF%1000))
    # print
    echo Temp: $(($TEMPF+$CARRYF)).$REMAINF F
}

echo Getting temp from hwmon0...
print_F `cat /sys/class/hwmon/hwmon0/temp1_input`

echo Getting temp from hwmon1...
print_F `cat /sys/class/hwmon/hwmon1/temp1_input`

echo Getting temp from hwmon2...
print_F `cat /sys/class/hwmon/hwmon2/temp1_input`