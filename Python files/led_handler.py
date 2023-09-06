
import board
import adafruit_dotstar as dotstar
import RPi.GPIO as GPIO
import numpy as np
import threading
import time
from typing import Tuple, Union

import handler
import modes.led_mode
import modes.default

n_dots = 240    #number of dots on a strip
ColorUnion = Union[int, Tuple[int, int, int], Tuple[int, int, int, int]]

class Led_Handler(handler.Handler):
    running = False

    def __init__(self, mode:modes.led_mode.Led_Mode = modes.default.mode, n_dots = 240) -> None:
        self.STATUS.change("Starting LED's")
        self.mode = mode
        self.MODE.change(self.mode.name)
        self.n_dots = n_dots

        self.dots = dotstar.DotStar(board.SCK, board.MOSI, n_dots, auto_write=False)
        self.flash_leds((0,255,0))
        
    def start(self) -> None:
        self.STATUS.change("Running")
        self.running = True
        self.mode.start(self)

    def stop(self) -> None:
        self.STATUS.change("Stopped")
        self.running = False
        self.mode.stop()
        time.sleep(self.mode.pace)
        self.clear_leds()

    def clear_leds(self) -> None:
        for i in range(self.n_dots):
            self.dots[i] = (0, 0, 0)
        self.dots.show()
    
    def flash_leds(self, color: ColorUnion) -> None:
        self.dots.fill(color)
        self.dots.show()
        time.sleep(0.2)
        self.dots.fill((0,0,0))
        self.dots.show()

    def change_mode(self, mode:modes.led_mode.Led_Mode):
        self.STATUS.change("Mode Change")
        self.running = False
        self.mode.stop()
        self.clear_leds()
        self.mode = mode
        self.MODE.change(self.mode.name)


def main():
    writer = Led_Handler()
    writer.start()
    threading.Timer(10, writer.stop).start()
    

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Keyboard interrupt")