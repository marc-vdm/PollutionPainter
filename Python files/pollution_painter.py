import os
import RPi.GPIO as GPIO
import threading

#self-build dependencies
import handlers.handler
import handlers.led_handler
import handlers.sensor_handler
import handlers.button_handler
import handlers.display_handler
import handlers.http_handler

import modes.default
import modes.faster

def console_status(status):
    print(f"Status Change: {status}")

#Initiating the handlers
context = handlers.handler.Handler()
context.STATUS.hook(console_status)
display = handlers.display_handler.Display_Handler()
sensor = handlers.sensor_handler.Sensor_Handler()
leds = handlers.led_handler.Led_Handler()
button = handlers.button_handler.button_handler()

def main():
    #threading.Thread(target=handlers.http_handler.start_server).start()
    button.press_callback = button_push
    button.longpress_callback = button_longpress
    button.double_press_callback = button_doublepress
    context.STATUS.change("Ready")
    


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

#Callback function for a longpress
#In this case darken the display and activity led
#Or vice versa

modes = [modes.default.mode, modes.faster.mode]
mode_iterator = 0

def button_doublepress():
    global mode_iterator
    mode_iterator = mode_iterator + 1
    if mode_iterator == len(modes): mode_iterator = 0
    leds.change_mode(modes[mode_iterator])

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        display.darken()
        leds.stop()
        pi_led_on()
        GPIO.cleanup()