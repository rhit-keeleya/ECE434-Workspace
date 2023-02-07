#!/usr/bin/env python3

import sheets
import timeit

path_prefix = "/sys/class/hwmon/hwmon"
path_suffix = "/temp1_input"
temps = []

def read_sensors():
    for i in range(3):
        file = open(path_prefix+ str(i) + path_suffix, "r")
        print(file.name)
        temp = file.read()
        temp = float(temp)/1000
        # convert to F
        temp = temp * 1.8 + 32
        # does some formatting
        temp = f'{temp:3.3f}'
        temps.append(temp)
        file.close()

start = timeit.default_timer()
read_sensors()
end = timeit.default_timer()
time = (end-start)

sheets.append_values(temps+[time    ])