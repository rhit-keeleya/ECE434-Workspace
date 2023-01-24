Files for HW07

# Project
TBD...

# Blynk

Skipped as was optional...

# 1-Wire Temperature Sensors

I noticed that my sensors appear to have the opposite pinout as that shown in the MAX31820 datasheet. When wired according to the datasheet, the sensors began to melt. This is generally not a good sign....

```
     .-""""""-.
   .'          '.
  /   O      O   \
 :           `    :
 |                |
 :    _-----_    :
  \  '        '  /
   '.          .'
     '-......-'
```


After I got the wiring sorted out, I ran "./temp.sh", and got output from all three sensors on P9_12. Then I tweaked the device tree file to work on P9_14 (see BB-W1-P9.14-00A0.dts), compiled, and tested it again. 

# Systemd

I modified the existing bb-code-server.service to launch the flask-based etch-a-sketch from HW04 (see online-etch-a-sketch.service).

# Blynk-based etch-a-sketch

I modified my previous etch-a-sketch program to be controllable via app using blynk. It can be run using "./blynk-etch-a-sketch.py". I then added it as a service to systemd, as it was more user friendly to control than the flask version of the etch-a-sketch.