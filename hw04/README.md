Files for HW04

# Memory Map
See mem_map.pdf to see the memory map for the BeagleBone

# GPIO via mmap
## switch2LEDs.c
Sets USR0/USR1 based on the inputs to P9_12 and P8_07, intended to be used with buttons wired to 3.3V.
Run with "sudo ./switch2LEDs".

## gpiotoggle.c
Toggle GPIO_60 (P9_12) as fast as possible by running "sudo ./gpiotoggle".

I saw an average period of 172us when using usleep(1), and average period of 360ns without usleep. For comparison, the fastest c script with gpiod had a period of about 3-4 us for me in hw02.

# I2C via Kernel Driver
Setup a TMP101 sensor on I2C bus 2, address 0x48 by running "./tempSetup.sh" as root.
Fetch the temperature by running "./temp.sh".

# Online Etch-a-sketch
Run with "./online-etch-a-sketch" and go to port 8081. Optionally, if an 8x8 LED matrix is connected, it will also show the etch-a-sketch on the matrix as well as the webserver.

# hw04 grading

| Points      | Description | |
| ----------- | ----------- | - |
|  2/2 | Memory map | *Nice pdf*
|  4/4 | mmap()
|  4/4 | i2c via Kernel
|  5/5 | Etch-a-Sketch via flask
|  5/5 | LCD display
|      | Extras
| 20/20 | **Total**
*Well done*
*My comments are in italics. --may*

