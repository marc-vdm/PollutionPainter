import os
import sys
import RPi.GPIO as GPIO

#self-build dependencies
import led_writer
import pm_sensor
import button_handler

#variables
PM25 = 0
sensor = pm_sensor.pm_sensor()
leds = led_writer.led_writer()
button = button_handler.button_handler()

def main():
    button.press_callback = button_push

def button_push():
    print("button push")
    if leds.running:
        leds.stop()
    else:
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