import os

def off():
    os.system('echo 0 | sudo tee /sys/class/leds/led0/brightness > /dev/null')

def on():
    os.system('echo 1 | sudo tee /sys/class/leds/led0/brightness > /dev/null')