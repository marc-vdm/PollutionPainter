
import board
import adafruit_dotstar as dotstar
import RPi.GPIO as GPIO
import numpy as np
import threading
import time
from typing import Tuple, Union

from ..misc import State
import modes.led_mode
import modes.default

n_dots = 240    #number of dots on a strip
ColorUnion = Union[int, Tuple[int, int, int], Tuple[int, int, int, int]]

class Led_Handler:
    running = False
    status = State("")

    def __init__(self, status) -> None:
        self.status = status
        self.status.change("Starting LED's")
        #self.mode.change(mode)
        #self.MODE.change(self.mode.name)
        self.n_dots = 240

        self.dots = dotstar.DotStar(board.SCK, board.MOSI, n_dots, auto_write=False)
        self.flash_leds((0,255,0))
    """    
    def start(self) -> None:
        self.status.change("Running")
        self.running = True
        self.mode.start(self)

    def stop(self) -> None:
        self.status.change("Stopped")
        self.running = False
        self.mode.stop()
        time.sleep(self.mode.pace)
        self.clear_leds()
    """
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

    """
    def change_mode(self, mode:modes.led_mode.Led_Mode):
        self.status.change("Mode Change")
        self.running = False
        self.mode.stop()
        self.clear_leds()
        self.mode = mode
        self.MODE.change(self.mode.name)
    """


def main():
    writer = Led_Handler(State("Testing"))
    writer.flash_leds((0,255,0))
    threading.Timer(10, writer.clear_leds).start()
    

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Keyboard interrupt")