import os
import RPi.GPIO as GPIO
import threading

#self-build dependencies
from modes import default, faster
from handlers import Led_Handler, Sensor_Handler, Button_Handler, Display_Handler, Mode_Handler, start_server
from misc import State, pi_led

def console_status(status):
    print(f"Status Change: {status}")

def main():
    status = State("Initiating")
    status.hook(console_status)
    display = Display_Handler(status)

    sensor = Sensor_Handler(status)
    sensor.pm25.hook(display.set_PM25)

    leds = Led_Handler(status)
    button = Button_Handler()

    modes = [default.mode, faster.mode]
    moderator = Mode_Handler(status, modes, display, sensor, leds, button)

    #Darken kit after button longpress
    def dark_switch():
        if display.darkened:
            display.restart()
            pi_led.on()
        else:
            display.darken()
            pi_led.off()
    
    button.longpress_callback = dark_switch
    

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        GPIO.cleanup()