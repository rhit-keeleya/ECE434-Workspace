// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
//
// Be sure to set -O3 when compiling.
// Modified by Mark A. Yoder  26-Sept-2013
// Adjusted GPIO pin and delays
// Modified by Abel Keeley  1/6/23 
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
 #include <unistd.h>
 #include <time.h>
#include "beaglebone_gpio.h"

/****************************************************************
 * Global variables
 ****************************************************************/
int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
	printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
	keepgoing = 0;
}

// function prototype
int getResponse(struct timespec* receive, struct timespec* send, volatile unsigned int* gpio_datain_addr);

int main(int argc, char *argv[]) {
    volatile void *gpio_addr;
    volatile unsigned int *gpio_oe_addr;
    volatile unsigned int *gpio_setdataout_addr;
    volatile unsigned int *gpio_cleardataout_addr;
    volatile unsigned int *gpio_datain_addr;
    unsigned int reg;
    struct timespec send;
    struct timespec receive;

    // want to toggle P9_13 or GPIO0_31
    // want to read P9_11 or GPIO0_30
    
    // Set the signal callback for Ctrl-C
	signal(SIGINT, signal_handler);
    // NOTE: stripped out the callback, as it would cause the program to hang when usleep was removed

    int fd = open("/dev/mem", O_RDWR);

    printf("Mapping %X - %X (size: %X)\n", GPIO0_START_ADDR, GPIO0_END_ADDR, GPIO0_SIZE);

    gpio_addr = mmap(0, GPIO0_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO0_START_ADDR);

    gpio_oe_addr           = gpio_addr + GPIO_OE;
    gpio_setdataout_addr   = gpio_addr + GPIO_SETDATAOUT;
    gpio_cleardataout_addr = gpio_addr + GPIO_CLEARDATAOUT;
    gpio_datain_addr   = gpio_addr + GPIO_DATAIN;

    if(gpio_addr == MAP_FAILED) {
        printf("Unable to map GPIO\nMay require sudo to memory map...\n");
        exit(1);
    }
    printf("GPIO mapped to %p\n", gpio_addr);
    printf("GPIO OE mapped to %p\n", gpio_oe_addr);
    printf("GPIO SETDATAOUTADDR mapped to %p\n", gpio_setdataout_addr);
    printf("GPIO CLEARDATAOUT mapped to %p\n", gpio_cleardataout_addr);

    // Set GPIO0_31 to output and GPIO0_30 to input
    reg = *gpio_oe_addr;
    printf("GPIO0 configuration: %X\n", reg);
    reg &= ~GPIO_31;        // Set GPIO0_31 bit to 0 for output
    reg |= GPIO_30;         // Set GPIO0_30 bit to 1 for input
    *gpio_oe_addr = reg;
    printf("GPIO0 configuration: %X\n", reg);

    // printf("Start blinking LED USR3\n");
    printf("Start toggling GPIO0_31 (P9_13)\n");
    while(keepgoing) {
        *gpio_setdataout_addr = GPIO_31;
        clock_gettime(CLOCK_MONOTONIC, &send);
        usleep(15);
        *gpio_cleardataout_addr = GPIO_31;

        if(getResponse(&receive,&send, gpio_datain_addr)==0) {
            // no response received for over a second
            printf("Uh-oh, timed out while waiting for receive signal!\n");
        } else {
            // response received
            long delta = receive.tv_nsec - send.tv_nsec;
            printf("Time delta between send and receive is %ld usec\n",delta/1000);
            usleep(600000);
        }
    }

    munmap((void *)gpio_addr, GPIO0_SIZE);
    close(fd);
    return 0;
}

int getResponse(struct timespec* receive, struct timespec* send, volatile unsigned int* gpio_datain_addr) {
    // initial implementation is with polling, will need to replace with interrupts
    struct timespec now;
    time_t delta  = 0; // time delta in sec
    while(delta<1) {
        // loop until delta >= 1sec OR receive signal
        clock_gettime(CLOCK_MONOTONIC, &now);
        delta = now.tv_sec - (*send).tv_sec; // update time delta
        if ((*gpio_datain_addr & GPIO_30)>>30==1) {
            // signal received, log time and return
            clock_gettime(CLOCK_MONOTONIC, receive);
            return 1;
        }
    }
    return 0;
}