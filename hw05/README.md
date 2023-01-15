Files for HW04

# Makefile
Completed the makefile exercise from [elinux](https://elinux.org/EBC_Exercise_15_make). The resulting makefile can be examined via "less Makefile".

# Kernel Source
Installed the 5.10.145 kernel.
>Linux BeagleBone2751 5.10.145-ti-r55 #1xross SMP PREEMPT Sat Jan 14 16:35:04 EST 2023 armv7l GNU/Linux

It's worth noting that this kernel version still doesn't support RTL8188FT wifi adapators out of the box.

# Cross-Compiling
Skipped per the note in the hw instructions

# Kernel Modules
Practiced with Derek Molloy's example modules, then modified gpio_test to support multiple buttons/LEDs. It expects LEDs on P9_27 and P9_23, and buttons connected to ground on P9_12 and P8_07. Insert the module with "sudo insmod gpio_test.ko" and remove it with "sudo rmmod gpio_test". The source code can be found in gpio_test.c

# ADXL345 Accelerometer
Added the adxl345 to I2C bus 2, address 0x53 via kernel driver. Interestingly enough, I previously had a tmp101 sensor on this address, and simply adding the adxl345 as a new device without first deleting the old device led to the new device not showing up properly (i.e. reading the name of the device would return adxl345, but iio:device1 would not appear). After deleting the old device, iio:device1 did show up as expected and contained the following contents:
>dev in_accel_x_calibbias in_accel_y_raw name subsystem in_accel_sampling_frequency in_accel_x_raw in_accel_z_calibbias power uevent in_accel_scale in_accel_y_calibbias in_accel_z_raw sampling_frequency_available

Also modified the etch-a-sketch program to be controlled via the accelerometer. The program expects both an 8x8 matrix and an ADXL345 accelerometer on i2c bus 2 (addresses 0x70 and 0x53, respectively). Run with "./accel-etch-a-sketch". Note: if no accelerometer detected, the program will attempt to set one up and may prompt for sudo privileges to do so.

# led.ko
Modified the led module to blink two LEDs (the gpio pins used are user configurable w/ module parameters). The second LED will blink at 1/2 the rate of the first. Can be inserted with "sudo insmod led.ko" and removed with "sudo rmmod led" - source code is in led.c