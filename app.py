from flask import Flask, render_template, Response, request
from threading import Thread
from time import sleep
from motorlib import motor


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

powerP = 0.6

#Setup for Right tank tread
#RightTread = motor("io1", 2, 9)
#rontRightFlipper = motor("io2", 1, 10)
#BackRightFlipper = motor("io1", 0, 0)

#Setup for Left tank tread
#LeftTread = motor("io1", 1, 10)
#FrontLeftFlipper = motor("io2", 2, 9)
#BackLeftFlipper = motor("io2", 0, 0)

#Setup for Turret
#Turret = motor("pi", 0, 0)

#Setup for Shoulder
#Shoulder = motor("pi", 0, 0)
#Shoulder2 = motor("pi", 0, 0)

#Setup for Elbow
#Elbow = motor("pi", 0, 0)

#Setup for Wrist
#Wrist = motor("pi", 0, 0)

#Setup for Claw
#Claw = motor("pi", 0, 0)

#app setup
app = Flask(__name__) 

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def index():  
   return render_template('gamepad.html')

@app.route('/mode_one', methods=['GET', 'POST'])
def mode_one():
   #this mode controls the treads, flippers
   if request.method == 'POST':

      
      joystick1 = request.form['joystick1']
      joystick2 = request.form['joystick2']

      frontLeftFlipperUp = bool(request.form['frontLeftFlipperUp'])
      frontLeftFlipperDown = bool(request.form['frontLeftFlipperDown'])

      frontRightFlipperUp = bool(request.form['frontRightFlipperUp'])
      frontRightFlipperDown = bool(request.form['frontRightFlipperDown'])

      backLeftFlipperUp = bool(request.form['backLeftFlipperUp'])
      backLeftFlipperDown = bool(request.form['backLeftFlipperDown'])

      backRightFlipperUp = bool(request.form['backRightFlipperUp'])
      backRightFlipperDown = bool(request.form['backRightFlipperDown'])


      joystick1 = int((float(joystick1)*100)*powerP)
      joystick2 = int((float(joystick2)*100)*powerP)

      '''
      LeftTread.start(joystick1)
      RightTread.start(joystick2)
      if joystick1 == 0:
         LeftTread.stop()
      if joystick2 == 0:
         RightTread.stop()
      print(joystick1)
      print(joystick2)
 
      if frontLeftFlipperUp == True:
         FrontLeftFlipper.start(25)
      if frontLeftFlipperDown == True:
         FrontLeftFlipper.start(-25)  
      if frontRightFlipperUp == True:
         FrontRightFlipper.start(25)
      if frontRightFlipperDown == True:
         FrontRightFlipper.start(-25)
      if backLeftFlipperUp == True:
        BackLeftFlipper.start(25)
      if backLeftFlipperDown == True:
         BackLeftFlipper.start(-25)
      if backRightFlipperUp == True:
         BackRightFlipper.start(25)
      if backRightFlipperDown == True:
         BackRightFlipper.start(-25)
      '''
      

      return render_template('gamepad.html')
   if request.method == 'GET':
      return render_template('gamepad.html')
   
@app.route('/mode_two', methods=['GET', 'POST'])
def mode_two():
   #this mode controls the turret, shoulder, elbow, wrist, claw
   if request.method == 'POST':

      turretControls = request.form['turretControls']

      shoulderControls = request.form['shoulderControls']

      elbowControls = request.form['elbowControls']

      wristControls = request.form['wristControls']


      # DOUBLE CHECK THESE
      #IDK IF VALUES FROM TRIGGERS ARE IN A 0-1 SCALE
      clawOpen = int(float(request.form['clawOpen'])*100)
      clawClose = int(float(request.form['clawClose'])*100)

      turret = int((float(turretControls)*100)*powerP)
      shoulder = int((float(shoulderControls)*100)*powerP)
      elbow = int((float(elbowControls)*100)*powerP)
      wrist = int((float(wristControls)*100)*powerP)

      '''
      Turret.start(turret)

      Shoulder.start(shoulder)
      Shoulder2.start(shoulder)

      Elbow.start(elbow)

      Wrist.start(wrist)

      if clawOpen == True:
         Claw.start(25)
      if clawClose == True:
         Claw.start(-25)
      '''

      return render_template('gamepad.html')
   if request.method == 'GET':
      return render_template('gamepad.html')

if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True, threaded=True)