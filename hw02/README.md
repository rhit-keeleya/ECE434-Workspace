# Homework 2

### togglegpio.sh
Questions:
1. What's the min and max voltage?

	Min = -45mV, Max = 3.306mV
2. What period and frequency is it?

	Period = 250ms, Frequency = 3.98Hz
3. How close is it to 100ms?

	Not very close at all!
4. Why do they differ?

	Maybe we are seeing overhead from using bash and sysfs to control the gpio.
5. Run htop and see how much processor you are using.

	Around 25% CPU usage.
6. Try different values for the sleep time (2nd argument). What's the shortest period you can get? Make a table of the fastest values you try and the corresponding period and processor usage. Try using markdown tables: https://www.markdownguide.org/extended-syntax/#tables
	
7. How stable is the period?

8. Try launching something like vi. How stable is the period?

9. Try cleaning up togglegpio.sh and removing unneeded lines. Does it impact the period?

10. Togglegpio.sh uses bash (first line in file). Try using sh. Is the period shorter?

11. What's the shortest period you can get?
