import time
from collections import deque
import serial
from sds011lib import SDS011QueryReader
import numpy as np
import threading
import state
import handler

class Sensor_Handler(handler.Handler):
    def __init__(self) -> None:
        self.STATUS.change("Starting Sensor")
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
            errorstring = "Startup Error: {}".format(e)
            self.STATUS.change(errorstring)
        
    def sample(self) -> float:
        return self.sensor.query().pm25
    
    def continuous_sampling(self) -> None:
        if self.cont_sample_flag:
            threading.Timer(1.01, self.continuous_sampling).start()
            PM25 = self.sample()
            self.PM25.change(PM25)
            self.buff.append(PM25)
            self.tbuff.append(time.time())
    
    def start_continuous_sampling(self) -> None:
        self.cont_sample_flag = True
        self.continuous_sampling()
                
    def stop_continuous_sampling(self) -> None:
        self.cont_sample_flag = False



def main():
    sensor = Sensor_Handler()
    time.sleep(10)
    #print(PM25)
    sensor.stop_continuous_sampling()
    

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Keyboard interrupt")