#!/usr/bin/env bash
# gpioToggle.sh	Abel Keeley	1/8/23
# Setup script for gpioToggle, configs triggers for usr leds and
# gpio pins

cd /sys/class/leds/beaglebone\:green\:usr0/
echo none > trigger
cd /sys/class/leds/beaglebone\:green\:usr1/
echo none > trigger
config-pin P9_12 gpio_pd
config-pin P8_07 gpio_pd
