#!/bin/bash

# hostname of the device we want to connect to.
HOSTNAME="BeagleBone2751"

IP=`host $HOSTNAME | awk '{print $NF}'`

./tunnel.sh $IP
