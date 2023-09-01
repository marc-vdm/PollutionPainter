
import board
import adafruit_dotstar as dotstar
import RPi.GPIO as GPIO
import numpy as np
import threading

PM25 = 5        #simulated PM25 value
n_dots = 240    #number of dots on a strip

x_points = np.linspace(0,550, num=2, endpoint=False)
y_points = np.linspace(0, 0.863, num=2, endpoint=False)

class led_writer():
    running = False

    def __init__(self, n_dots = 240) -> None:
        self.n_dots = n_dots

        if 'PM25' not in globals():
            raise Exception("No global PM25 variable found during led_writer initialization")

        self.dots = dotstar.DotStar(board.SCK, board.MOSI, n_dots, auto_write=False)
        print("init led writer")
        
    def start(self) -> None:
        self.running = True
        self.loop()

    def stop(self) -> None:
        self.running = False
        threading.Timer(0.1, self.clear_leds).start()
    
    def loop(self) -> None:
        #Start next loop in 0.1 seconds
        if(self.running):
            threading.Timer(0.1, self.loop).start()

        #calculate cutoff and p from PM25 value
        prob=np.interp(PM25, x_points, y_points)

        #Set leds with new probability
        self.set_leds(prob)

    
    def set_leds(self, p) -> None:
        #Create a list of n_dots size with random True False values
        rand_list = np.random.choice([False, True], size=(self.n_dots,), p=[1-p, p])

        for i in range(self.n_dots):
            if rand_list[i]:
                self.dots[i] = (255, 255, 255)
            else:
                self.dots[i] = (0, 0, 0)
        self.dots.show()
    
    def clear_leds(self) -> None:
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
        print("Keyboard interrupt")