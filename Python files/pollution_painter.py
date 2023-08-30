import os
import sys
import threading
import RPi.GPIO as GPIO
import time
from sds011lib import SDS011QueryReader
import serial
from collections import deque
import numpy as np
import threading

#led_writer dependencies
from .led_writer import led_writer

user = os.getuid()
if user != 0:
    print("Please run script as root")
    sys.exit()
    
class pm_sensor(object):
    def __init__(self) -> None:
        self.startup_sensor()

        self.buff = deque(np.zeros(5, dtype='f'), 5)
        self.tbuff = deque(np.zeros(5, dtype='f'), 5)
        time.sleep(1)

        self.cont_sample_flag = True
        self.start_continuous_sampling()

    def startup_sensor(self) -> None:
        try:
            self.sensor = SDS011QueryReader('/dev/ttyUSB0')
            self.port = serial.Serial("/dev/ttyAMA0", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0)
        except Exception as e:
            global STATUS
            errorstring = "Startup Error: {}".format(e)
            print (errorstring)
        
    def sample(self) -> float:
        return self.sensor.query().pm25
    
    def continuous_sampling(self) -> None:
        if self.cont_sample_flag:
            self.buff.append(self.sample())
            self.tbuff.append(time.time())
    
    def start_continuous_sampling(self) -> None:
        threading.Timer(1.01, self.continuous_sampling()).start()        
    
    def stop_continuous_sampling(self) -> None:
        self.cont_sample_flag = False


leds = led_writer()


def button(channel):
    print("button pressed")
    #Code after buttonpress here!

def loop():
    #threading.Timer(1.0, loop).start()
    pass

def main():
    #Code to set-up button GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(6, GPIO.FALLING, callback=button, bouncetime=1000)

    
    pm_sens = pm_sensor()
    
    #start main loop
    loop()

if __name__ == '__main__':
    try:        
        print('Starting up')
        #Below are server threads for interacting with the board later
        #threading.Thread(target=run_osc_server).start()
        #threading.Thread(target=run_http_server).start()
        main()

    except KeyboardInterrupt:
        GPIO.cleanup()