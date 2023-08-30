
import board
import adafruit_dotstar as dotstar
import RPi.GPIO as GPIO
import numpy as np
import threading

PM25 = 5        #simulated PM25 value
n_dots = 240    #number of dots in a strip

x_points = np.linspace(0,550, num=2, endpoint=False)
y_points = np.linspace(0, 0.863, num=2, endpoint=False)

class led_writer():
    running = False

    def __init__(self, n_dots = 240):
        self.n_dots = n_dots

        self.dots = dotstar.DotStar(board.SCK, board.MOSI, n_dots, auto_write=False)
        print("init led writer")
        
    def start(self):
        self.running = True
        self.loop()

    def stop(self):
        self.running = False
        threading.Timer(0.1, self.clear_leds).start()
    
    def loop(self):
        #Start next loop in 0.1 seconds
        if(self.running):
            threading.Timer(0.1, self.loop).start()

        #calculate cutoff and p from PM25 value
        prob=np.interp(PM25, x_points, y_points)
        print(prob)

        #Set leds with new probability
        self.set_leds(prob)

    
    def set_leds(self, p):
        #Create a list of n_dots size with random True False values
        rand_list = np.random.choice([False, True], size=(self.n_dots,), p=[1-p, p])

        for i in range(self.n_dots):
            if rand_list[i]:
                self.dots[i] = (255, 255, 255)
            else:
                self.dots[i] = (0, 0, 0)
        self.dots.show()
    
    def clear_leds(self):
        for i in range(self.n_dots):
            self.dots[i] = (0, 0, 0)
        self.dots.show()


def main():
    writer = led_writer()
    writer.start()
    threading.Timer(10, writer.stop).start()
    

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        #GPIO.cleanup()
        print("Keyboard interrupt")