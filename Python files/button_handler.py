import time
import board
import digitalio
import threading



class button_handler():
    button = digitalio.DigitalInOut(board.D9)
    pressed_time = time.time()
    released_time = time.time()

    press_callback: function | None = None
    longpress_callback: function | None = None
    button_down_callback: function | None = None
    button_up_callback: function | None = None
    double_press_callback: function | None = None

    def __init__(self) -> None:
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

        threading.Thread(target=self.released).start()

    def released(self) -> None:
        #Callback function for button coming up
        self.button_up_method()

        #Loop that breaks when button is pressed
        while self.button.value:
            continue
        
        #return to pressed loop
        self.pressed()
    
    def pressed(self) -> None:
        #Callback function for button coming down
        self.button_down_method()

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
            self.longpress_method()
        #If the time between presses is shorter than 0.5s callback
        elif delta_released_time < 0.3:
            self.press_timer.cancel() #Cancel the normal press
            self.double_press_method()
        #If not start a threading Timer for a normal press, that can
        #be canceled in case of a double press
        else:
            self.press_timer = threading.Timer(0.4, self.press_method)
            self.press_timer.start()

        #return to released loop
        self.released()
    
    def press_method(self) -> None:
        if self.press_callback != None:
            self.press_callback.__func__()
        pass

    def longpress_method(self) -> None:
        if self.longpress_callback != None:
            self.longpress_callback.__func__()
        pass

    def button_down_method(self) -> None:
        if self.button_down_callback != None:
            self.button_down_callback.__func__()
        pass

    def button_up_method(self) -> None:
        if self.button_up_callback != None:
            self.button_up_callback.__func__()
        pass

    def double_press_method(self) -> None:
        if self.double_press_callback != None:
            self.double_press_callback.__func__()
        pass


def main():
    button_handler()

    button_handler.press_callback = callback

def callback():
    print("press callback")

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Keyboard interrupt")