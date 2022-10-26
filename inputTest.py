import RPi.GPIO as GPIO			# using Rpi.GPIO module
from time import sleep			# import function sleep for delay

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
p2 = GPIO.PWM(AN2, 100)			# set pwm for M2

def Forward():
    print("Forward")
    GPIO.output(DIG1, GPIO.LOW)
    GPIO.output(DIG2, GPIO.LOW)
    p1.start(100)
    p2.start(100)

def Left():
    print("Left")
    GPIO.output(DIG1, GPIO.HIGH)
    GPIO.output(DIG2, GPIO.LOW)
    p1.start(100)
    p2.start(100)

def Right():
    print("Right")
    GPIO.output(DIG1, GPIO.LOW)
    GPIO.output(DIG2, GPIO.HIGH)
    p1.start(100)
    p2.start(100)

def Backward():
    print("Backward")
    GPIO.output(DIG1, GPIO.HIGH)
    GPIO.output(DIG2, GPIO.HIGH)
    p1.start(100)
    p2.start(100)

def Decel():
    print("Decel")
    p1.start(80)
    p2.start(80)
    sleep(0.5)
    p1.start(60)
    p2.start(60)
    sleep(0.5)
    p1.start(40)
    p2.start(40)
    sleep(0.5)
    p1.start(20)
    p2.start(20)
    sleep(0.5)
    p1.start(0)
    p2.start(0)
    sleep(0.5)

def Accel():
    print("Accel")
    p1.start(0)
    p2.start(0)
    sleep(0.5)
    p1.start(20)
    p2.start(20)
    sleep(0.5)
    p1.start(40)
    p2.start(40)
    sleep(0.5)
    p1.start(60)
    p2.start(60)
    sleep(0.5)
    p1.start(80)
    p2.start(80)
    sleep(0.5)
    p1.start(100)
    p2.start(100)
    sleep(0.5)

#print("f - Forward")
#print("l - Left")
#print("r - Right")
#print("b - Backward")

def main():

    print("f - Forward")
    print("l - Left")
    print("r - Right")
    print("b - Backward")


    x=input("Enter Choice: ")

    if (x == "f"):
        Accel()
        Forward()
        Decel()
        main()
    elif (x == "l"):
        Accel()
        Left()
        Decel()
        main()
    elif (x == "r"):
        Accel()
        Right()
        Decel()
        main()
    elif (x == "b"):
        Accel()
        Backward()
        Decel()
        main()
    else:
        print("Not a valid option")
        Decel()
        main()

