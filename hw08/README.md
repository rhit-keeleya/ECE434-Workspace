Files for HW08

Note: was going for an A, see the table of results at the bottom.

# Blinking an LED

After getting the starter code (hello.pru0.c) up and running, I modified it to toggle P9_31 (see hello_P9_31.pru0.c). Then I removed the delay and made some measurements - see the results section below.

Note: Can use "sudo make <stop/start> TARGET=.pru<0/1>" to stop/start the corresponding pru.

# Controlling PWM frequency

The pwm4 program uses P9_31, P9_29, P9_30, and P9_28 as output pins. This corresponds to bit 0-3 of R30 for pru0. Saw a max frequency of 326.8KHz. I could successfully alter the frequency of the pwm, bringing it down to ~86kHz.

# Results

|Test|Period|Notes|
|--|--|--|
|Toggling P9_31 GPIO via pru0|80ns|Not a lot of jitter, seeing a std dev of 230ps. Not too surprising seeing as this is the only thing running on the pru.|
|PWM @ 50MHz on P9_31 via pru0 registers|20ns|Seeing some visual jitter here with a std dev of 44 ps.|
|4-Channel PWM| 3us| Trying to do 4-channel pwm (and reading values from memory) is very slow compared to just 1, hardcoded, channel.|
|4-Channel PWM, after updating delays| 11.6us| Very steady output, almost no visible jitter.|
|Input-Output @ 3MHz| 333ns | Bit of jitter on both input and output. Measured an offset of about 40 ns using onscreen cursors.|
|Digital DAC| 163us | Made a pretty nice sine wave using a lowpass filter... got some ugly intermittent distortion, not sure why.|