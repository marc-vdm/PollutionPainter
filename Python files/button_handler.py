import time
import board
import digitalio
import threading

from collections.abc import Callable



class button_handler():
    button = digitalio.DigitalInOut(board.D9)
    pressed_time = time.time()
    released_time = time.time()

    press_callback: Callable[[],None] | None = None
    longpress_callback: Callable[[],None] | None = None
    button_down_callback: Callable[[],None] | None = None
    button_up_callback: Callable[[],None] | None = None
    double_press_callback: Callable[[],None] | None = None

    def __init__(self) -> None:
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

        threading.Thread(target=self.__released).start()

    def __released(self) -> None:
        #Callback function for button coming up
        self.__button_up_method()

        #Loop that breaks when button is pressed
        while self.button.value:
            continue
        
        #return to pressed loop
        self.__pressed()
    
    def __pressed(self) -> None:
        #Callback function for button coming down
        self.__button_down_method()

        #Recording time between last release and this press for 
        #possible double-press
        self.pressed_time = time.time()
        delta_released_time = self.pressed_time - self.released_time

        #Loop that breaks when button is released
        while not self.button.value:
            continue

        #Recording time between last press and this release for
        #possible long-press
        self.released_time = time.time()
        delta_pressed_time = self.released_time - self.pressed_time

        #If the press-duration is longer than 1s callback
        if delta_pressed_time > 1:
            self.__longpress_method()
        #If the time between presses is shorter than 0.5s callback
        elif delta_released_time < 0.2:
            self.press_timer.cancel() #Cancel the normal press
            self.__double_press_method()
        #If not start a threading Timer for a normal press, that can
        #be canceled in case of a double press
        else:
            self.press_timer = threading.Timer(0.4, self.__press_method)
            self.press_timer.start()

        #return to released loop
        self.__released()
    
    def __press_method(self) -> None:
        if self.press_callback != None:
            self.press_callback()
        pass

    def __longpress_method(self) -> None:
        if self.longpress_callback != None:
            self.longpress_callback()
        pass

    def __button_down_method(self) -> None:
        if self.button_down_callback != None:
            self.button_down_callback()
        pass

    def __button_up_method(self) -> None:
        if self.button_up_callback != None:
            self.button_up_callback()
        pass

    def __double_press_method(self) -> None:
        if self.double_press_callback != None:
            self.double_press_callback()
        pass


def main():
    button = button_handler()

    button.press_callback = press_callback
    button.longpress_callback = longpress_callback
    button.double_press_callback = double_press_callback
    #button.button_up_callback = button_up_callback
    #button.button_down_callback = button_down_callback

def press_callback():
    print("press callback")

def longpress_callback():
    print("longpress callback")

def double_press_callback():
    print("doublepress callback")

def button_up_callback():
    print("button up callback")

def button_down_callback():
    print("button down callback")

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Keyboard interrupt")