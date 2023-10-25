import threading

class Led_Mode():
    def __init__(self, name: str, pace: float, led_function):
        self.name = name
        self.pace = pace
        self.led_function = led_function
    
    def __loop(self, Led_Handler, Sensor_Handler):
        self.timer = threading.Timer(self.pace, self.__loop, [Led_Handler, Sensor_Handler])
        self.timer.start()
        self.led_function(Led_Handler, Sensor_Handler)
    
    def __clear(self, Led_Handler):
        Led_Handler.clear_leds()

    def start(self, Led_Handler, Sensor_Handler):
        self.__loop(Led_Handler, Sensor_Handler)

    def stop(self):
        try:
            #self.timer.cancel()
            self.timer.function = self.__clear
        except:
            print("Mode had no timer init yet.")