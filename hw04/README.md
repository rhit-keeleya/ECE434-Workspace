Files for HW04

#Memory Map
See mem_map.pdf to see the memory map for the BeagleBone

#GPIO via mmap
##

##gpiotoggl.c
Toggle GPIO_60 (P9_12) as fast as possible by running "sudo ./gpiotoggle".

I saw an average period of 172us when using usleep(1), and average period of 360ns without usleep. For comparison, the fastest c script with gpiod had a period of about 3-4 us for me in hw02.
