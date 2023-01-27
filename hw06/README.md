Files for HW06

# Responses to "What Every Driver Developer Should Know about RT"

1.	Julia Cartwright works at National Instruments.
2.	Preempt RT is the RT patch for the Linux Kernel. The big takeaway is that it removes all unbounded latencies.
3.	Mixed criticality is when you have two (or more) tasks running with different criticalities. This could also apply when you have systems that communicate/interact that are themselves of different criticalities.
4.	One set of driver misbehavior is when the driver disables local IRQs - this can balloon IRQ dispatch latency. Another type of misbehavior is when drivers disable preemption temporarily, which prevents the scheduler from switching to the higher priority thread after the interrupt has fired.
5.	The delta from Figure 1 is the delay between an event occuring and the application that handles that event being started.
6.	Cyclictest measures the difference between intended and actual wakeup time for a thread. It can provide statistics about the system's latency.
7.	Figure 2 shows a histogram of the latencies measured by Cyclictest for Preempt vs Preempt RT running on identical hardware.
8.	IRQ dispatch latency is the delay between an event happening and the scheduler being notified. Scheduling latency is the delay between the schedular being made aware of the event and the thread that will handle the event being woken.
9.	Mainline is the, well, mainline Linux Kernel - no forks, no additional patches.
10.	Well, the interrupt handler is still executing from the previous interrupt. The external event won't interrupt until the previous handler is finished.
11.	With Preempt RT, each interrupt handler just serves to wake a thread, that thread then executes the code that responds to the interrupt. Since all the interrupt handler does is wake a thread, it finishes and allows the external event to trigger an interrupt much sooner.

# Cyclictest Results

I ran the cyclic test with both an rt and non-rt kernel under two conditions: no load and loaded. The load was provided by running ./timeWaster.sh which contained a loop that printed out the number of times the loop had been executed. The resulting histograms can be found in no_load_cyclictest.png and loaded_cyclictest.png

Looking at the results, it seems that the rt kernel has a bounded latency of 150us.

# hw06 grading

| Points      | Description | |
| ----------- | ----------- |-|
|  2/2 | Project | *IoT Entry Cam*
|  5/5 | Questions | *What's the part about M18?*
|  4/4 | PREEMPT_RT | *Wow, your timewaste really wasted time*
|  2/2 | Plots to 500 us
|  5/5 | Plots - Heavy/Light load
|  2/2 | Extras
| 20/20 | **Total**

*My comments are in italics. --may*
