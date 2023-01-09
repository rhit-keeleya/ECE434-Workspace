#!/usr/bin/env bash
# tempSetup.sh       Abel Keeley     1/8/23

# setup device
cd /sys/class/i2c-adapter/i2c-2/
sudo echo tmp101 0x48 > new_device
