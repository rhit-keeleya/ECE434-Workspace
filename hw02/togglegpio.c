#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>

// Run "gcc togglegpio.c -o togglegpio" to compile

void toggleGPIO();

int main( int argc, char *argv[] )  {
	float delay = atof(argv[2]);
	if( argc == 3 ) {
		printf("Toggling GPIO pin %s with delay %.6f ms.\n", argv[1],delay);
	}
	else {
	printf("Expected two arguments: Pin and Delay.\n");
	}
	char path2[] = "/sys/class/gpio/gpio";
	strcat(path2,argv[1]);
    strcat(path2,"/value");
	char toggle = 0;
	char *value = (toggle) ? "1" : "0";
	int fd = open(path2, O_RDWR| O_NONBLOCK );
	while(1){
		write(fd, value, 2);
		lseek(fd, 0, SEEK_SET);
		usleep(delay*1000);
		toggle = toggle^1;
		value = (toggle) ? "1" : "0";
	}
	return(0);
}