from re import U
from flask import Flask, render_template, Response, request
from time import sleep
from static import stepper

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Setup for Right tank tread
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

#Setup for Left tank tread
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

#Setup for Turret
AN5 = 26
DIG5 = 20
GPIO.setup(AN5, GPIO.OUT)
GPIO.setup(DIG5, GPIO.OUT)
p5 = GPIO.PWM(AN5, 100)

#Setup for Shoulder & Elbow respectively

AN6 = 19
DIG6 = 16
GPIO.setup(AN6, GPIO.OUT)
GPIO.setup(DIG6, GPIO.OUT)
p6 = GPIO.PWM(AN6, 100)
AN7 = 0
DIG7 = 0
GPIO.setup(AN7, GPIO.OUT)
GPIO.setup(DIG7, GPIO.OUT)
p7 = GPIO.PWM(AN7, 100)


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
      turretClockwise = request.form['turretClockwise']
      turretCounterClockwise = request.form['turretCounterClockwise']
      elbowUp = request.form['elbowUp']
      elbowDown = request.form['elbowDown']
      shoulderUp = request.form['shoulderUp']
      shoulderDown = request.form['shoulderDown']
      joystick1 = int((float(joystick1)*100))
      joystick2 = int((float(joystick2)*100))
      print("Left % power",joystick1)
      print("Right % power",joystick2)
      print("Turret Clockwise",turretClockwise)
      print("Turret Counter Clockwise",turretCounterClockwise)
      print("Elbow Up",elbowUp)
      print("Elbow Down",elbowDown)
      print("Shoulder Up",shoulderUp)
      print("Shoulder Down",shoulderDown)


      #Left tread
      if joystick1 < 0:
         joystick1 = -joystick1
         GPIO.output(DIG1, GPIO.HIGH)
         GPIO.output(DIG2, GPIO.LOW)
         p1.start(joystick1)
         p2.start(joystick1)
      else:
         GPIO.output(DIG1, GPIO.LOW)
         GPIO.output(DIG2, GPIO.HIGH)
         p1.start(joystick1)
         p2.start(joystick1)

      #Right tread 
      if joystick2 < 0:
         joystick2 = -joystick2
         GPIO.output(DIG3, GPIO.LOW)
         GPIO.output(DIG4, GPIO.HIGH)
         p3.start(joystick2)
         p4.start(joystick2)
      else:
         GPIO.output(DIG3, GPIO.HIGH)
         GPIO.output(DIG4, GPIO.LOW)
         p3.start(joystick2)
         p4.start(joystick2)
      
      #Turret
      if turretClockwise == True and turretCounterClockwise == False:
         GPIO.output(DIG5, GPIO.HIGH)
         p5.start(30)
         sleep(0.2)
         p5.start(60)
      elif turretCounterClockwise == True and turretClockwise == False:
         GPIO.output(DIG5, GPIO.LOW)
         p5.start(30)
         sleep(0.2)
         p5.start(60)
      else:
         p5.stop()
      #Shoulder & Elbow
      
      if shoulderUp == True and shoulderDown == False:
         GPIO.output(DIG6, GPIO.HIGH)
         p6.start(30)
         sleep(0.2)
         p6.start(60)
      elif shoulderDown == True and shoulderUp == False:
         GPIO.output(DIG6, GPIO.LOW)
         p6.start(30)
         sleep(0.2)
         p6.start(60)
      else:
         p6.stop()
      if elbowUp == 1 and elbowDown == 0:
         GPIO.output(DIG7, GPIO.HIGH)
         p7.start(30)
         sleep(0.2)
         p7.start(60)
      elif elbowDown == 1 and elbowUp == 0:
         GPIO.output(DIG7, GPIO.LOW)
         p7.start(30)
         sleep(0.2)
         p7.start(60)
      else:
         p7.stop()
      
   return render_template('gamepad.html')

if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True, threaded=True)