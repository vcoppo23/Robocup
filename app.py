from re import U
from flask import Flask, render_template, Response, request
from time import sleep
from static import stepper

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Setup for one tank tread
AN2 = 23
AN1 = 22
DIG2 = 18
DIG1 = 17
GPIO.setup(AN2, GPIO.OUT)
GPIO.setup(AN1, GPIO.OUT)
GPIO.setup(DIG2, GPIO.OUT)
GPIO.setup(DIG1, GPIO.OUT)
p1 = GPIO.PWM(AN1, 100)
p2 = GPIO.PWM(AN2, 100)
#Setup for second tank tread
AN4 = 9
AN3 = 11
DIG4 =25
DIG3 =8
GPIO.setup(AN4, GPIO.OUT)
GPIO.setup(AN3, GPIO.OUT)
GPIO.setup(DIG4, GPIO.OUT)
GPIO.setup(DIG3, GPIO.OUT)
p3 = GPIO.PWM(AN3, 100)
p4 = GPIO.PWM(AN4, 100)


app = Flask(__name__) 

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def index(): 
   if request.method == 'POST':    
      return render_template('gamepad.html')
   else:
      return render_template('gamepad.html')

@app.route('/forward', methods=['GET', 'POST'])
def forward():
   if request.method == 'POST':

      joystick1 = request.form['joystick1']
      joystick2 = request.form['joystick2']
      joystick1 = int((float(joystick1)*100)/3)
      joystick2 = int((float(joystick2)*100)/3)
      print("Left % power",joystick1)
      print("Right % power",joystick2)
      #Left tread
      if joystick1 < 0:
         joystick1 = -joystick1
         GPIO.output(DIG1, GPIO.HIGH)
         GPIO.output(DIG2, GPIO.HIGH)
         p1.start(joystick1)
         p2.start(joystick1)
      else:
         GPIO.output(DIG1, GPIO.LOW)
         GPIO.output(DIG2, GPIO.LOW)
         p1.start(joystick1)
         p2.start(joystick1)
      #Right tread 
      if joystick2 < 0:
         joystick2 = -joystick2
         GPIO.output(DIG2, GPIO.HIGH)
         GPIO.output(DIG3, GPIO.HIGH)
         GPIO.output(DIG4, GPIO.HIGH)
         p3.start(joystick2)
         p4.start(joystick2)
      else:
         GPIO.output(DIG2, GPIO.LOW)
         GPIO.output(DIG3, GPIO.LOW)
         GPIO.output(DIG4, GPIO.LOW)
         p3.start(joystick2)
         p4.start(joystick2)
         
      
   return render_template('gamepad.html')

if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True, threaded=True)