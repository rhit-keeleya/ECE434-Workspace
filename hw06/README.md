Files for HW04

# Responses to "What Every Driver Developer Should Know about RT"

1.	Julia Cartwright works at National Instruments.
2.	Preempt RT is the RT patch for the Linux Kernel. The big takeaway is that it removes all unbounded latencies.
3.	Mixed criticality is when you have two (or more) tasks running with different criticalities. This could also apply when you have systems that communicate/interact that are themselves of different criticalities.
4.	One set of driver misbehavior is when the driver disables local IRQs - this can balloon IRQ dispatch latency. Another type of misbehavior is when drivers disable preemption temporarily, which prevents the scheduler from switching to the higher priority thread after the interrupt has fired.
5.	The delta from Figure 1 is the delay between an event occuring and the application that handles that event being started.
6.	Cyclictest measures the difference between intended and actual wakeup time for a thread. It can provide statistics about the system's latency.
7.	Figure 2 shows a histogram of the latencies measured by Cyclictest for Preempt vs Preempt RT running on identical hardware.
8.	IRQ dispatch latency is the delay between an event happening and the scheduler being notified. Scheduling latency is the delay between the schedular being made aware of the event and the thread that will handle the event being woken.
9.	Mainline is the, well, mainline Linux Kernel - no forks, no additional patches.1.	Check the status of the M18 battery and verify it is not in over discharged (single indicator light flashing) or over heated state (indicator lights flashing in an alternating pattern). If it is over discharged, connect it to a charger and allow it to charge up to at least 25% (1/4 indicator bars on) before proceeding. If it is over heated, allow it to cool off and recheck the status.
10.	Well, the interrupt handler is still executing from the previous interrupt. The external event won't interrupt until the previous handler is finished.
11.	With Preempt RT, each interrupt handler just serves to wake a thread, that thread then executes the code that responds to the interrupt. Since all the interrupt handler does is wake a thread, it finishes and allows the external event to trigger an interrupt much sooner.
