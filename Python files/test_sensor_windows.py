import time
from sds011lib import SDS011QueryReader


class pm_sensor(object):
    pm25 = 1
    def __init__(self) -> None:
        self.startup_sensor()

        time.sleep(1)
        #self.take_sample()


    def startup_sensor(self) -> None:
        try:
            self.sensor = SDS011QueryReader('/dev/ttyUSB0')
            self.port = serial.Serial("/dev/ttyAMA0", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0)
        except Exception as e:
            global STATUS
            errorstring = "Startup Error: {}".format(e)
            print (errorstring)
        
    def take_sample(self):
        t = time.time()
        print('should be getting sample now')
        sample = self.sensor.query().pm25
        print('the sample is :', type(sample), sample)

pm_sensor() 
