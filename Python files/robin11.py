import serial
from sds011lib import SDS011QueryReader
from serial import Serial
import spidev
import opc
import time
from time import sleep
from datetime import datetime
#from neopixel import *
from collections import deque
from scipy import interpolate
#from scipy.interpolate import interp1d
import numpy as np
import random
import os
import sys
# from papirus import Papirus
# from PIL import Image
# from PIL import ImageDraw
# from PIL import ImageFont
import RPi.GPIO as GPIO
import threading
import random
import math
from pythonosc import udp_client
import argparse
from pythonosc import dispatcher
from pythonosc import osc_server
from typing import List, Any

#Marin's stuff | KEEP OUT
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

user = os.getuid()
if user != 0:
	print("Please run script as root")
	sys.exit()

# LED strip configuration:
LED_COUNT      = 219      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255       # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
#LED_STRIP      = ws.WS2811_STRIP_GRB

# Command line usage
# papirus-buttons

WHITE = 1
BLACK = 0

SIZE = 27

SW1 = 26
SW2 = 19
SW3 = 20
SW4 = 16
SW5 = 21
SW6 = 6

#papirus = Papirus()

DRAWING = 0
TIME_STARTED = 0
TIME_STOPPED = 0

PM25 = 0
DUMMY_PM25 = 10
DUMMY_MODE = 0
LOGGING = 1

STATUS = "Booting"

buff = deque(np.zeros(5, dtype='f'), 5)
tbuff = deque(np.zeros(5, dtype='f'), 5)

x_points = np.linspace(0,550, num=256, endpoint=False)
y_points = np.linspace(255,45, num=256, endpoint=False)

just_started = False
just_stopped = False
got_brightness = False
got_wait = False
got_fade = False

brightness = 30

sending = False

def brightness_handler(address: str, *args: List[Any]) -> None:
	if not len(args)== 1 or type(args[0]) is not float:
		global got_brightness
		global brightness
		got_brightness = True
		brightness = int(args[1])
		print("recieved OSC /brightness {}".format(brightness))
		client.send_message("/brightness", brightness)

def wait_handler(address: str, *args: List[Any]) -> None:
	if not len(args)== 1 or type(args[0]) is not float:
		global got_wait
		global wait
		got_wait = True
		wait = int(args[1])
		print("recieved OSC /wait {}".format(wait))
		client.send_message("/wait", wait)

def fade_handler(address: str, *args: List[Any]) -> None:
	if not len(args)== 1 or type(args[0]) is not float:
		global got_fade
		global fade
		got_fade = True
		fade = int(args[1])
		print("recieved OSC /fade {}".format(fade))
		client.send_message("/fade", fade)

def manualmode_handler(address: str, *args: List[Any]) -> None:
	print(address)
	print(args)
	print(len(args))
	print(type(args[0]))
	print(type(args[1]))
	if not len(args)== 1 or type(args[0]) is not float:
		global DUMMY_MODE
		if args[1] == 1:
			DUMMY_MODE = True
			print("set DUMMY_MODE = True")
		else:
			DUMMY_MODE = False
			print("set DUMMY_MODE = False")


def manualPM25_handler(address: str, *args: List[Any]) -> None:
	if not len(args)== 1 or type(args[0]) is not float:
		global DUMMY_PM25
		DUMMY_PM25 = int(args[1])
		print("recieved OSC /manualPM25 {}".format(DUMMY_PM25))
		client.send_message("/manualPM25", DUMMY_PM25)


# def shutdown(channel):

# 	try:
# 		write_text(papirus, "Shutting Down", SIZE)
# 		print("shutdown button pressed")
# 		sleep(2)
# 		os.system("sudo shutdown -h now")
# 		#Send command to system to shutdown
# 	except:
# 		pass

# 	GPIO.cleanup()

# def button1(channel):
# 	global PM25
# 	global DUMMY_MODE
# 	#awrite_text(papirus, "PM2.5 " + '%.2f' %PM25 + " ug/m^3", SIZE)
# 	print("button 1 pressed")
# 	DUMMY_MODE = False

def command_out(command):
	global sending
	sending = True
	global port
	correct_response = False
	attempts = 0
	while correct_response == False and attempts < 8:
		#print("sending " + command)
		port.flushInput()
		port.flushOutput()
		bytes_out = port.write(command.encode('utf-8'))
		attempts = attempts + 1
		sleep(0.1)
		response = "<" + port.read(bytes_out).decode('utf-8') + ">"
		#print("got response " + response)
		if response == command:
			correct_response = True
			

	if not correct_response:
		global STATUS
		print("failed to send {} to arduino".format(command))
		STATUS = "failed to send {} to arduino".format(command)
	sending = False

def button2(channel):
	global DRAWING
	global TIME_STOPPED
	global TIME_STARTED
	global just_started
	global just_stopped
	global STATUS
	if (DRAWING==1):
		DRAWING = 0
		TIME_STOPPED = time.time()
		#print("stop")
		#command_out("<stop>")
		just_stopped = True
		STATUS = "Stopping"
	else:
		DRAWING = 1
		TIME_STARTED = time.time()
		#command_out("<start>")
		#print("start")
		just_started = True
		STATUS = "Starting"
	print("button2 pressed")

# def button3(channel):
# 	global DUMMY_PM25
# 	global DUMMY_MODE
# 	DUMMY_PM25 += 10
# 	write_text(papirus, "dPM2.5 " + '%.2f' %DUMMY_PM25 + " ug/m^3", SIZE)
# 	DUMMY_MODE = True
# 	print("button3 pressed")

# def button4(channel):
# 	global DUMMY_PM25
# 	global DUMMY_MODE
# 	DUMMY_PM25 -= 10
# 	write_text(papirus, "dPM2.5 " + '%.2f' %DUMMY_PM25 + " ug/m^3", SIZE)
# 	DUMMY_MODE = True
# 	print("button4 pressed")

# def button5(channel):
# 	global COLOR_MODE
# 	if (COLOR_MODE == 0):
# 		COLOR_MODE = 1
# 		write_text(papirus, "COLOUR MODE ON", SIZE)
# 	else:
# 		COLOR_MODE = 0
# 		write_text(papirus, "COLOUR MODE OFF", SIZE)
# 	print("button5 pressed")

def f(x, b, t):
	y_points = np.array(list(b))
	x_points = np.array(list(t))
	#x_points = np.linspace(0, 4, num=5, endpoint=True)
	#tck = interpolate.splrep(x_points, y_points)
	#return interpolate.splev(x, tck)
	#g = interp1d(x_points, y_points, kind='cubic')
	return np.interp(x, x_points, y_points)


def f2(x, b, t):
	y_points = np.array(list(b))
	x_points = np.array(list(t))
	tck = interpolate.splrep(x_points, y_points)
	return interpolate.splev(x, tck)

def map(value, start1, stop1, start2, stop2):
	output = float(start2) + float((value - start1)) / float((stop1 - start1)) * float((stop2 - start2))
	return int(output)

# def write_text(papirus, text, size):

# 	# initially set all white background
# 	image = Image.new('1', papirus.size, WHITE)

# 	# prepare for drawing
# 	draw = ImageDraw.Draw(image)

# 	font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)

# 	# Calculate the max number of char to fit on line
# 	line_size = (papirus.width / (size*0.65))

# 	current_line = 0
# 	text_lines = [""]

# 	# Compute each line
# 	for word in text.split():
# 		# If there is space on line add the word to it
# 		if (len(text_lines[current_line]) + len(word)) < line_size:
# 			text_lines[current_line] += " " + word
# 		else:
# 			# No space left on line so move to next one
# 			text_lines.append("")
# 			current_line += 1
# 			text_lines[current_line] += " " + word

# 	current_line = 0
# 	for l in text_lines:
# 		current_line += 1
# 		draw.text( (0, ((size*current_line)-size)) , l, font=font, fill=BLACK)

# 	papirus.display(image)
# 	papirus.update()

def sample():
	threading.Timer(1.0, sample).start()
	global buff,tbuff, PM25, DRAWING, sensor, client
	#histogram = alpha.histogram()
	aqi = sensor.query()
	test_time = time.time()
	#pm25 = histogram['PM2.5']
	pm25 = aqi.pm25
	if (pm25):
		#print("PM2.5 " + str(pm25) + " ug/m^3")
		global PM25
		PM25 = pm25
		tbuff.append(test_time)
		buff.append(PM25)
		client.send_message("/PM25", f'{PM25:.2f}')

def loop():
	threading.Timer(1.0, loop).start()
	global just_started
	global just_stopped
	global got_brightness
	global brightness
	global got_wait
	global wait
	global got_fade
	global fade
	global sending
	global STATUS
	if not sending:
		if just_started:
			command_out("<start>")
			just_started = False
			STATUS = "Doing Magic"
		if just_stopped:
			command_out("<stop>")
			just_stopped = False
			STATUS = "Stopped"
		if got_brightness:
			command_out("<brightness " + str(brightness).zfill(3) + ">")
			got_brightness = False
		if got_wait:
			command_out("<wait " + str(wait).zfill(3) + ">")
			got_wait = False
		if got_fade:
			command_out("<fade " + str(fade).zfill(4) + ">")
			got_fade = False

		interpolated_PM25 = (f(time.time() - 1, buff, tbuff))
		#print("interpolated_PM25 = {}".format(interpolated_PM25))
		if (True):
			if (DUMMY_MODE == True):
				interpolated_PM25 = DUMMY_PM25
			cutoff=int(np.interp(interpolated_PM25, x_points, y_points))

			command_out("<cutoff " + str(cutoff).zfill(3) + ">")

			client.send_message("/cutoff", cutoff)

def main():
    GPIO.setmode(GPIO.BCM)

    #GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(SW5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SW6, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)

    #GPIO.add_event_detect(SW1, GPIO.RISING, callback=button1)
    #GPIO.add_event_detect(SW2, GPIO.RISING, callback=button3)
    #GPIO.add_event_detect(SW3, GPIO.RISING, callback=button4)
    #GPIO.add_event_detect(SW4, GPIO.RISING, callback=button5)
    #GPIO.add_event_detect(SW5, GPIO.RISING, callback=shutdown)
    GPIO.add_event_detect(SW6, GPIO.FALLING, callback=button2, bouncetime=1000)

    
    try:
        global sensor
        sensor = SDS011QueryReader('/dev/ttyUSB0')
        global port
        port = serial.Serial("/dev/ttyAMA0", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0)
    except Exception as e:
        global STATUS
        errorstring = "Startup Error: {}".format(e)
        print (errorstring)
        STATUS = errorstring
	
        #write_text(papirus, "Script Error", SIZE)

    sleep(2)
    test_time = time.time()
    display_update = time.time()

    sample()
    loop()

#GUI Stuff below

class HttpRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('info.html', 'rb') as file:
                self.wfile.write(file.read())
	    
        elif self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'pm25': PM25, 'status':STATUS}
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run_http_server():
    server_address = ('', 80)
    httpd = HTTPServer(server_address, HttpRequestHandler)
    print('Running HTTP server on port 80...')
    httpd.serve_forever()

def run_osc_server():
    global client
    client = udp_client.SimpleUDPClient("192.168.12.255", 9000, True)
    dispatcher2 = dispatcher.Dispatcher()
    dispatcher2.map("/brightness", brightness_handler, "brightness")
    dispatcher2.map("/wait", wait_handler, "wait")
    dispatcher2.map("/fade", fade_handler, "fade")
    dispatcher2.map("/manualmode", manualmode_handler, "manualmode")
    dispatcher2.map("/manualPM25", manualPM25_handler, "manualPM25")
    server = osc_server.ThreadingOSCUDPServer(("192.168.12.1", 7777), dispatcher2)
    print("Running OSC server on port 7777...")
    server.serve_forever()

if __name__ == '__main__':
	try:		
		print('Starting up')
		threading.Thread(target=run_osc_server).start()
		threading.Thread(target=run_http_server).start()
		main()

	except KeyboardInterrupt:
		GPIO.cleanup()

