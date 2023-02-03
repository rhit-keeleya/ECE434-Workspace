Files for HW09

# Project Timeline

|Milestone|Description|Target Date|Completed?|
|-|-|-|-|
|1|By M1, the camera system should be able to reliably alert the user if motion is detected.| N/A | Yes|
|2|By M2, the camera system should be able to generate a link that the user can follow to a webserver capable of serving images/video of any motion events captured.|2/6/23| No|
|3|By M3, the camera system should be able allow the user to remotely select whether to save any videos or pictures permanently (as of now, they are written to /tmp/ and would be lost if the system is powercycled). | 2/13/23| No|
|4|By M4, the camera system should be complete, including a nice UI. | 2/20/23| No|

# Logging
The script "one_wire_temp.py" will attempt to open hwmon0 - hwmon2 and log all three temperatures + the execution time of the read_sensors() function to google sheets. I added a cron job to fire the script every minute, and I'm planning on letting it run over night. The data gathered can be found [here](https://docs.google.com/spreadsheets/d/1qzS6IE8V2jU31syVeEl5ryPkoYs4Zy2su7EB0obKXb8/edit#gid=0), and looks something like this:


Sensor 3 is close to the Beagle, while 1 and 2 are at the other end of the breadboard - note the consistent temperature difference there!