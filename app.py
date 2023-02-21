from flask import Flask, render_template, Response, request
from threading import Thread
from time import sleep
from motorlib import motor, objectlist, stopall, shutdown
from subprocess import call

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

powerP = 0.6

#Setup for Right tank tread
RightTread = motor("io1", 1, 10)
FrontRightFlipper = motor("io1", 6, 12)
#BackRightFlipper = motor("io1", 0, 0)

#Setup for Left tank tread
LeftTread = motor("io1", 2, 8)
FrontLeftFlipper = motor("io1", 5, 11)
#BackLeftFlipper = motor("io2", 0, 0)

#Setup for Turret
#Turret = motor("io2", 2, 8)

#Setup for Shoulder
#Shoulder = motor("io2", 1, 10)


#Setup for Elbow
#Elbow = motor("io2", 5, 11)

#Setup for Wrist
#Wrist = motor("io2", 6, 12)

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

      endLife = (request.form['shutdown'])

      joystick1 = request.form['joystick1']
      joystick2 = request.form['joystick2']

      frontLeftFlipperUp = (request.form['frontLeftFlipperUp'])
      frontLeftFlipperDown = (request.form['frontLeftFlipperDown'])

      frontRightFlipperUp = (request.form['frontRightFlipperUp'])
      frontRightFlipperDown = (request.form['frontRightFlipperDown'])

      backLeftFlipperUp = (request.form['backLeftFlipperUp'])
      backLeftFlipperDown = (request.form['backLeftFlipperDown'])

      backRightFlipperUp = (request.form['backRightFlipperUp'])
      backRightFlipperDown = (request.form['backRightFlipperDown'])


      joystick1 = int((float(joystick1)*100)*powerP)
      joystick2 = int((float(joystick2)*100)*powerP)

      if endLife  == 'true': ##shutsdown all motors and turns the pi off
         shutdown()

      
      #LeftTread.start(joystick1)
      #RightTread.start(joystick2)
      
      FrontLeftFlipper.start(joystick1)
      FrontRightFlipper.start(joystick2)
      '''
      if frontLeftFlipperUp == 'true':
         FrontLeftFlipper.start(60)
      else:
         FrontLeftFlipper.start(0)

      if frontLeftFlipperDown == 'true':
         FrontLeftFlipper.start(-60)  
      else:
         FrontLeftFlipper.start(0)

      if frontRightFlipperUp == 'true':
         FrontRightFlipper.start(60)
      else:
         FrontRightFlipper.start(0)

      if frontRightFlipperDown == 'true':
         FrontRightFlipper.start(-60)
      else:
         FrontRightFlipper.start(0)
      
      if backLeftFlipperUp == 'true':
        BackLeftFlipper.start(25)
      else: 
         BackLeftFlipper.start(0)

      if backLeftFlipperDown == 'true':
         BackLeftFlipper.start(-25)
      else:
         BackLeftFlipper.start(0)

      if backRightFlipperUp == 'true':
         BackRightFlipper.start(25)
      else:
         BackRightFlipper.start(0)

      if backRightFlipperDown == 'true':
         BackRightFlipper.start(-25)
      else:
         BackRightFlipper.start(0)
      '''
      
      print(f"{joystick1} power, {joystick2} power")

      return render_template('gamepad.html')
   if request.method == 'GET':
      return render_template('gamepad.html')
   
@app.route('/mode_two', methods=['GET', 'POST'])
def mode_two():
   #this mode controls the turret, shoulder, elbow, wrist, claw
   if request.method == 'POST':
      
      endLife2 = (request.form['shutdown2'])

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
      if endLife2 == 'true':  ##shutsdown all motors and turns the pi off 
         shutdown()
      
      Turret.start(turret)

      Shoulder.start(shoulder)
      

      Elbow.start(elbow)

      Wrist.start(wrist)

      #if clawOpen == True:
      #   Claw.start(25)
      #if clawClose == True:
      #   Claw.start(-25)
      

      #print(f"{clawOpen} power, {clawClose} power")
      '''
      return render_template('gamepad2.html')
   if request.method == 'GET':
      return render_template('gamepad2.html')

if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True, threaded=True)