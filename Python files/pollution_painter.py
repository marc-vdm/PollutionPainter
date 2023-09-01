import os
import sys
import RPi.GPIO as GPIO

#self-build dependencies
import led_writer
import pm_sensor

#variables
PM = 0

def main():
    leds = led_writer.led_writer()
    sensor = pm_sensor.pm_sensor()
    leds.start()

if __name__ == '__main__':
    try:        
        print('Starting up')
        """
        if os.getuid() != 0:
            print("Please run script as root")
            sys.exit()
        """
        main()

    except KeyboardInterrupt:
        GPIO.cleanup()