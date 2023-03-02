import json
from flask import Flask, render_template, Response, request
from threading import Thread
from time import sleep
from motorlib import motor, objectlist, stopall, shutdown
from subprocess import call

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

powerP = 0.6

#hi gabe -tommy
#Setup for Right tank tread
RightTread = motor("io1", 1, 9)
FrontRightFlipper = motor("io1", 5, 11)
#BackRightFlipper = motor("io1", 0, 0)

#Setup for Left tank tread
LeftTread = motor("io1", 2, 10)
FrontLeftFlipper = motor("io1", 6, 12)
#BackLeftFlipper = motor("io2", 0, 0)

#Setup for Turret
Turret = motor("io2", 2, 10)

#Setup for Shoulder
Shoulder = motor("io2", 1, 9)


#Setup for Elbow
Elbow = motor("io2", 5, 11)

#Setup for Wrist
Wrist = motor("io2", 6, 12)

#Setup for Claw
#Claw = motor("pi", 0, 0)

#app setup
app = Flask(__name__) 

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def index():  
   return render_template('gamepad3.html')

def valueConverter(value):
   if value == 'true':
      return True
   else:
      return False

@app.route('/mode_one', methods=['GET', 'POST'])
def mode_one():
   #this mode controls the treads, flippers
   while request.method == 'POST':

      dictionary = json.loads(request.POST.get('values'))

      print(dictionary)

      endLife = dictionary['shutdown']

      joystick1 = dictionary['joystick1']
      joystick2 = dictionary['joystick2']

      frontLeftFlipperUp = dictionary['frontLeftFlipperUp']
      frontLeftFlipperDown = dictionary['frontLeftFlipperDown']

      frontRightFlipperUp = dictionary['frontRightFlipperUp']
      frontRightFlipperDown = dictionary['frontRightFlipperDown']

      backLeftFlipperUp = dictionary['backLeftFlipperUp']
      backLeftFlipperDown = dictionary['backLeftFlipperDown']

      backRightFlipperUp = dictionary['backRightFlipperUp']
      backRightFlipperDown = dictionary['backRightFlipperDown']


      joystick1 = int((float(joystick1)*100)*powerP)
      joystick2 = int((float(joystick2)*100)*powerP)

      if endLife  == 'true': ##shutsdown all motors and turns the pi off
         while True:
            LeftTread.start(0)
            RightTread.start(0)
            FrontLeftFlipper.start(0)
            FrontRightFlipper.start(0)
            #BackLeftFlipper.stop()
            #BackRightFlipper.stop()

      LeftTread.start(joystick1)
      RightTread.start(-joystick2)
      
      if valueConverter(frontLeftFlipperUp):
         FrontLeftFlipper.start(50)
      elif valueConverter(frontLeftFlipperDown):
         FrontLeftFlipper.start(-50)  
      else:
         FrontLeftFlipper.start(0)

      if valueConverter(frontRightFlipperUp):
         FrontRightFlipper.start(-50)
      elif valueConverter(frontRightFlipperDown):
         FrontRightFlipper.start(50)
      else:
         FrontRightFlipper.start(0)

      #if valueConverter(backLeftFlipperUp):
         #BackLeftFlipper.start(50)
      #elif valueConverter(backLeftFlipperDown):
         #BackLeftFlipper.start(-50)
      #else:
         #BackLeftFlipper.start(0)

      #if valueConverter(backRightFlipperUp):
         #BackRightFlipper.start(50)
      #elif valueConverter(backRightFlipperDown):
         #BackRightFlipper.start(-50)
      #else:
         #BackRightFlipper.start(0)
      
      return render_template('gamepad3.html')
   else:
      LeftTread.start(0)
      RightTread.start(0)
      FrontLeftFlipper.start(0)
      FrontRightFlipper.start(0)
      #BackLeftFlipper.start()
      #BackRightFlipper.start()
      return render_template('gamepad3.html')

   
@app.route('/mode_two', methods=['GET', 'POST'])
def mode_two():
   #this mode controls the turret, shoulder, elbow, wrist, claw
   while request.method == 'POST':

      dictionary = json.loads(request.POST.get('values'))

      endLife2 = dictionary['shutdown']

      turretControls = dictionary['turretControls']

      shoulderControls = dictionary['shoulderControls']

      elbowControls = dictionary['elbowControls']

      wristControls = dictionary['wristControls']

      clawOpen = int(float(dictionary['clawOpen'])*100)
      clawClose = int(float(dictionary['clawClose'])*100)

      turret = int((float(turretControls)*100)*powerP)
      shoulder = int((float(shoulderControls)*100)*powerP)
      elbow = int((float(elbowControls)*100)*powerP)
      wrist = int((float(wristControls)*100)*powerP)
      
      if endLife2 == 'true':  ##shutsdown all motors and turns the pi off 
         while True:
            Turret.start(0)
            Shoulder.start(0)
            Elbow.start(0)
            Wrist.start(0)
            #Claw.start(0)
      
      Turret.start(turret)

      Shoulder.start(-shoulder)
      
      Elbow.start(elbow)

      Wrist.start(-wrist)

      #Claw.start(clawOpen-clawClose)
      
      return render_template('gamepad3.html')
   else:
      Turret.start(0)
      Shoulder.start(0)
      Elbow.start(0)
      Wrist.start(0)
      #Claw.start(0)
      return render_template('gamepad3.html')

if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True, threaded=True)