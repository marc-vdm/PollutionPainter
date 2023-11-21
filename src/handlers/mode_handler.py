from misc import State, pi_led
from modes import default

import os


class Mode_Handler:
    running = False
    mode_iterator = 0

    def __init__(self, status, mode_list, display_handler, sensor_handler, led_handler, button_handler):
        self.status = status

        self.mode_list = mode_list

        self.display_handler = display_handler
        self.sensor_handler = sensor_handler
        self.led_handler = led_handler
        self.button_handler = button_handler

        self.mode = State(mode_list[self.mode_iterator])

        button_handler.press_callback = self.stop_go
        button_handler.double_press_callback = self.switch
    
    def stop_go(self):
        if not self.running:
            self.running = True
            self.status.change("Running...")

            self.display_handler.darken()
            pi_led.off()

            mode = self.mode.variable
            mode.start(self.led_handler, self.sensor_handler)
        else:
            self.running = False
            self.status.change("Stopped...")

            self.display_handler.restart()
            pi_led.on()

            self.mode.variable.stop()
    
    def switch(self):
        self.status.change("Mode Change")
        self.mode.variable.stop()

        self.mode_iterator = self.mode_iterator + 1
        if self.mode_iterator == len(self.mode_list): self.mode_iterator = 0

        self.mode.change(self.mode_list[self.mode_iterator])

