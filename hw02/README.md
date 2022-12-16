# Homework 2

### switch2led.py

Run "./switch2led.py". Pressing any of the push buttons will light the corresponding LED.

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

| Sleep Time (ms) | Period (ms) |
|-|-|
|100|250|
|10|70|
|1|53|
|0.1|51|

9. How stable is the period?

	+/-1ms
8. Try launching something like vi. How stable is the period?

	+/-4ms	
9. Try cleaning up togglegpio.sh and removing unneeded lines. Does it impact the period?

	Yes, dropped the period down from ~50ms to ~23ms.
10. Togglegpio.sh uses bash (first line in file). Try using sh. Is the period shorter?

	Yes, dropped the period down from ~23ms to ~16ms.
11. What's the shortest period you can get?

	~16ms.

### togglegpio.py

Questions:

1. What period and frequency is it?
	Period = 202ms, Frequency = 4.9Hz
2. Run htop and see how much processor you are using.
	CPU usage is about 5%.
3. Present the shell script and Python script results in a table for easy comparison.

| Sleep Time (ms) | Script Period (ms) | Python Period|
|-|-|-|
|100|250|202|
|10|70|22.4|
|1|53|4.3|
|0.1|51|1.3|
|0.01|-|1.2|

### togglegpio.c
Note: Use "gcc togglegpio.c -o togglegpio" to compile the program.

Questions:

1. What period and frequency is it?
	Period = 200.7ms, Frequency = 4.98Hz
2. Run htop and see how much processor you are using.
	CPU usage is about 5%.
3. Present the shell script, Python script, and C script results in a table for easy comparison.

| Sleep Time (ms) | Script Period (ms) | Python Period| C Period|
|-|-|-|-|
|100|250|202|200|
|10|70|22.4|20.8|
|1|53|4.3|2.6|
|0.1|51|1.3|0.4|
|0.01|-|1.2|0.2|

### gpiod

| Sleep Time (ms) | Script Period (ms) | Python Period| C Period| toggle1.py (gpiod) | toggle1.c (gpiod) | toggle2.py (gpiod) | toggle2.c (gpiod) |
|-|-|-|-|-|-|-|-|
|100|250|202|200|201|200.5|201|200.5|
|10|70|22.4|20.8|20.9|20.7|20.9|20.6|
|1|53|4.3|2.6|2.9|2.6|2.9|2.6|
|0.1|51|1.3|0.4|0.4|0.4|0.45|0.4|
|0.01|-|1.2|0.2|0.2|0.2|0.25|0.21|
|0|-|-|-|0.018|0.004|0.018|0.003|

### getsetEvent.py

Run "./getsetEvent.py". Like before, push any button and the corresponding LED will light.

### Etch-a-sketch-buttons.py

Run the program w/ "./etch-a-sketch-buttons.py" and follow the instructions on screen!

# hw02 grading

| Points      | Description |
| ----------- | ----------- |
|  2/2 | Buttons and LEDs 
|  8/8 | Etch-a-Sketch works
|      | Measuring a gpio pin on an Oscilloscope 
|  2/2 | Questions answered
|  4/4 | Table complete
|  2/2 | gpiod
|      | Security
|  0/1 | ssh port 
|  0/1 | fail2ban
| 19/20   | **Total**

ssh port change and fail2ban are missing.

Nicelyy done tables.  +1