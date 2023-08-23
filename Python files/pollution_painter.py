import os
import sys
import threading
import RPi.GPIO as GPIO

user = os.getuid()
if user != 0:
	print("Please run script as root")
	sys.exit()
	

def button(channel):
	print("button pressed")
	#Code after buttonpress here!

def loop():
	threading.Timer(1.0, loop).start()

def main():
    #Code to set-up button GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(6, GPIO.FALLING, callback=button, bouncetime=1000)

    
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
	
    #start main loop
    loop()

if __name__ == '__main__':
	try:		
		print('Starting up')
		#Below are server threads for interacting with the board later
		#threading.Thread(target=run_osc_server).start()
		#threading.Thread(target=run_http_server).start()
		main()

	except KeyboardInterrupt:
		GPIO.cleanup()