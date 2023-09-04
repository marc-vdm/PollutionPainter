import os
import RPi.GPIO as GPIO

#self-build dependencies
import led_handler
import sensor_handler
import button_handler
import display_handler

#Initiating the handlers
display = display_handler.Display_Handler()
sensor = sensor_handler.Sensor_Handler()
leds = led_handler.Led_Handler()
button = button_handler.button_handler()

def main():
    button.press_callback = button_push
    button.longpress_callback = button_longpress
    display.STATUS.change("Ready")
    

#Callback function for a single button push
#In this case darken the display and activity led
#Start running the ledstrip, or vice versa
def button_push():
    if leds.running:
        leds.stop()
        display.restart()
        pi_led_on()
    else:
        leds.start()
        display.darken()
        pi_led_off()

#Callback function for a longpress
#In this case darken the display and activity led
#Or vice versa
def button_longpress():
    if display.darkened:
        display.restart()
        pi_led_on()
    else:
        display.darken()
        pi_led_off()

#Functions for turning the activity led of the pi on and off
def pi_led_off():
    os.system('echo 0 | sudo tee /sys/class/leds/led0/brightness > /dev/null')

def pi_led_on():
    os.system('echo 1 | sudo tee /sys/class/leds/led0/brightness > /dev/null')

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        display.darken()
        leds.stop()
        pi_led_on()
        GPIO.cleanup()