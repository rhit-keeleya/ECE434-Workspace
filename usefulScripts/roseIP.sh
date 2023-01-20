#!/bin/bash

# hostname of the device we want to connect to.
HOSTNAME="BeagleBone2751"

IP=`host $HOSTNAME.rose-hulman.edu | awk '{print $NF}'`

./tunnel.sh $IP
