# HomeWork #3

### Reading T101s

Note: assumes T101s are on i2cbus 2, addresses 0x48 and 0x49

For a shell script that reads T101 outputs, run "./temp.sh"

For a python script that reads T101 outputs and periodically updates them, run "./temp.py"

For a python script that reads T101 outputs *on interrupt*, run "./tempAlert.py" <- Assumes alert pins are on P9_11 and P9_13

### etch-a-sketch

Made a tri-color etch-a-sketch in python. It has a few dependencies - needs two rotary encoders on P8_11, P8_12 and P_33, P_35, respectively, for controls. Displays on an led matrix on i2c bus 2, address 0x70. Uses a couple T101 sensors (addresses 0x48 and 0x49) on i2c bus 2 to erase the etch-a-sketch and/or change the pen color. The alert lines from those sensors should be on P9_11 and P9_13. The program will show the temp from each sensor as well as the trigger temp on screen. Run it with "./rotary-etch-a-sketch".

Note: may need to adjust the event temperature to properly erase/change color. For best results put it about 1 degree above ambient 

# hw03 grading

| Points      | Description | | |
| ----------- | ----------- |-|-|
|  8/8 | TMP101 
|  2/2 |   | Documentation 
|  5/5 | Etch-a-Sketch
|  3/3 |   | setup.sh | *Nice use of system()command to setup*
|  2/2 |   | Documentation
| 20/20 | **Total**

*My comments are in italics. --may*

