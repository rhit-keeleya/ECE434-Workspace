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
Practiced with Derek Molloy's example modules, then modified gpio_test to support multiple buttons/LEDs. It expects LEDs on P9_27 and P9_23, and buttons connected to ground on P9_12 and P8_07. Insert the module with "sudo insmod gpio_test.ko". The source code can be found in gpio_test.c

