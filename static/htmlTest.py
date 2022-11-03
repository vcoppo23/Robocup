#import RPi.GPIO as GPIO			# using Rpi.GPIO module
from time import sleep			# import function sleep for delay
def setup():
	GPIO.setmode(GPIO.BCM)			# GPIO numbering
	GPIO.setwarnings(False)			# enable warning from GPIO
	AN2 = 23 				# set pwm2 pin on MD10-Hat
	AN1 = 22				# set pwm1 pin on MD10-hat
	DIG2 = 18 				# set dir2 pin on MD10-Hat
	DIG1 = 17  				# set dir1 pin on MD10-Hat
	GPIO.setup(AN2, GPIO.OUT)		# set pin as output
	GPIO.setup(AN1, GPIO.OUT)		# set pin as output
	GPIO.setup(DIG2, GPIO.OUT)		# set pin as output
	GPIO.setup(DIG1, GPIO.OUT)		# set pin as output
	sleep(1)				   # delay for 1 seconds
	p1 = GPIO.PWM(AN1, 100)			# set pwm for M1
	p2 = GPIO.PWM(AN2, 100)
	print("Setup Complete")
def forward():
	i = 10
	#GPIO.output(DIG1, GPIO.LOW)
    #GPIO.output(DIG2, GPIO.LOW)
	while i<100:
		#p1.start(i)
		#p2.start(i)
		print("Speed is at ",i, "%")
		i+=10
		sleep(0.25)
	if i==100:
		print("Holding for 3 seconds")
		sleep(3)
		while 0<=i<=100:
			#p1.start(i)
			#p2.start(i)
			print("Speed is at ",i,"%")
			i-=10
			sleep(0.25)
	else:
		print("It's Val's fault")
def backward():
	i = 10
	#GPIO.output(DIG1, GPIO.HIGH)
    #GPIO.output(DIG2, GPIO.HIGH)
	while i<100:
		#p1.start(i)
		#p2.start(i)
		print("Speed is at ",i,"%")
		i+=10
		sleep(0.25)
	if i==100:
		print("Holding for 3 seconds")
		sleep(3)
		while 0<=i<=100:
			#p1.start(i)
			#p2.start(i)
			print("Speed is at ",i,"%")
			i-=10
			sleep(0.25)
	else:
		print("It's Val's fault")