/*  switch2LEDs.c    Abel Keeley 1/8/23
    Sets USR0/USR1 LEDs based on button (connected to 3.3V) inputs to P9_12 and P8_07.
    Build with "cc -o switch2LEDs switch2LEDs.c"
*/
#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>
#include <signal.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

// generic GPIO stuff
#define GPIO_SIZE 0x2000
#define GPIO_OE_OFFSET 0x134
#define GPIO_DATAIN_OFFSET 0x138
#define GPIO_SETDATAOUT_OFFSET 0x194
#define GPIO_CLEARDATAOUT_OFFSET 0x190

// specific GPIO chips being used
#define GPIO1_START_ADDR 0x4804C000
#define GPIO2_START_ADDR 0x481AC000

// specific pins being used
#define USR0 (1<<21)
#define USR1 (1<<22)
#define BUTTON1 (1<<28)
#define BUTTON2 (1<<2)

// setup script to run
#define SETUP "./gpioToggle.sh"

int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig){
	printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
	keepgoing = 0;
}

int main() {
    volatile void *gpio1_addr;
    volatile void *gpio2_addr;

    signal(SIGINT, signal_handler);
    int fd = open("/dev/mem", O_RDWR);
    system(SETUP);
    // map the GPIO ports to be used
    gpio1_addr = mmap(NULL, GPIO_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO1_START_ADDR);
    gpio2_addr = mmap(NULL, GPIO_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO2_START_ADDR);

    if(gpio1_addr == MAP_FAILED | gpio2_addr == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        printf("Error number is: %d\n",errno);
        printf("File descriptor is %d\n",fd);
        printf("May need to run with sudo to have necessary file permissions...")
        exit(1);
    }

    // assuming map worked, don't need fd anymore
    close(fd);
    // set USR leds to be outputs
    *(volatile unsigned int *)(gpio1_addr+GPIO_OE_OFFSET) = *(volatile unsigned int *)(gpio1_addr+GPIO_OE_OFFSET) & ~(USR0 | USR1);
    // set buttons to be inputs
    *(volatile unsigned int *)(gpio1_addr+GPIO_OE_OFFSET) = *(volatile unsigned int *)(gpio1_addr+GPIO_OE_OFFSET) | BUTTON1;
    *(volatile unsigned int *)(gpio2_addr+GPIO_OE_OFFSET) = *(volatile unsigned int *)(gpio2_addr+GPIO_OE_OFFSET) | BUTTON2;

    while(keepgoing){
        int b1 = (*(volatile unsigned int *)(gpio1_addr+GPIO_DATAIN_OFFSET) & BUTTON1)>>28;
        int b2 = (*(volatile unsigned int *)(gpio2_addr+GPIO_DATAIN_OFFSET) & BUTTON2)>>2;
        
        if(b1 == 1) *(volatile unsigned int *)(gpio1_addr+GPIO_SETDATAOUT_OFFSET) = USR0;
        else *(volatile unsigned int *)(gpio1_addr+GPIO_CLEARDATAOUT_OFFSET) = USR0;

        if(b2 == 1) *(volatile unsigned int *)(gpio1_addr+GPIO_SETDATAOUT_OFFSET) = USR1;
        else *(volatile unsigned int *)(gpio1_addr+GPIO_CLEARDATAOUT_OFFSET) = USR1;

        // printf("BUTTON1 = %x, BUTTON2 = %x\n",b1,b2);
        usleep(10000);
    }

    munmap((void *)gpio1_addr, GPIO_SIZE);
    return 0;
}