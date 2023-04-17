from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json as JSON
from colorama import Fore
import os
from motorlib import *
import RPi.GPIO as GPIO
from encoder import Encoder

#Setup Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Setup Expander Boards
io1 = board(0x18)
io2 = board(0x19)

#Setup Motors
RightTread = motor(io1, 1, 9)
RightTreadEncoder = Encoder(18, 23)
gear_ratio = int(input("Enter the gear ratio of the right tread: "))
FrontRightFlipper = motor(io1, 5, 11)
BackRightFlipper = motor(io1, 1, 9)

LeftTread = motor(io1, 2, 10)
FrontLeftFlipper = motor(io1, 6, 12)
BackLeftFlipper = motor(io2, 1, 9)

Turret = motor(io2, 2, 10)

Shoulder = motor(io2, 1, 9)

Elbow = motor(io2, 5, 11)

Wrist = motor(io2, 6, 12)

Claw = motor("pi", 1, 9)

#Setup Power Variables
powerP = 0.6
powerT = 0.6

def Shutdown(message):
    if message == "true":
        #Sets all motors to 0
        RightTread.start(0)
        FrontRightFlipper.start(0)
        BackRightFlipper.start(0)
        LeftTread.start(0)
        FrontLeftFlipper.start(0)
        BackLeftFlipper.start(0)
        Turret.start(0)
        Shoulder.start(0)
        Elbow.start(0)
        Wrist.start(0)
        Claw.start(0)
    elif message == "false":
        pass

def valueConverter(value):
   if value == 'true':
      return True
   else:
      return False  


@app.route('/')
def index():
    return render_template('gamepad3.html')

@socketio.on('connect')
def test_connect():
    print(Fore.GREEN + 'Client connected' + Fore.RESET)

@socketio.on('disconnect')
def test_disconnect():
    print(Fore.RED + 'Client disconnected' + Fore.RESET)

    #Stops all motors incase of disconnect
    shutdown = "true"
    Shutdown(shutdown)

@socketio.on('treads')
def my_event(message):
    #os.system('clear')
    #print(str(message))

    #Checks for shutdown
    shutdown = message['shutdown']
    Shutdown(shutdown)

    LeftTread.start(int((float(message['joystick1'])*100)*powerP))
    RightTread.start(int((float(message['joystick2'])*100)*powerP))
    
    print(((RightTreadEncoder.getValue()*360)/(7 * gear_ratio)))

    if valueConverter(message['frontLeftFlipperUp']):
         FrontLeftFlipper.start(50)
    elif valueConverter(message['frontLeftFlipperDown']):
        FrontLeftFlipper.start(-50)  
    else:
        FrontLeftFlipper.start(0)

    if valueConverter(message['frontRightFlipperUp']):
        FrontRightFlipper.start(-50)
    elif valueConverter(message['frontRightFlipperDown']):
        FrontRightFlipper.start(50)
    else:
        FrontRightFlipper.start(0)
    '''
    if valueConverter(message['backLeftFlipperUp']):
        BackLeftFlipper.start(50)
    elif valueConverter(message['backLeftFlipperDown']):
        BackLeftFlipper.start(-50)
    else:
        BackLeftFlipper.start(0)
    if valueConverter(message['backRightFlipperUp']):
        BackRightFlipper.start(50)
    elif valueConverter(message['backRightFlipperDown']):
        BackRightFlipper.start(-50)
    else:
        BackRightFlipper.start(0)'''
    
    print("LeftPower: " + str(int((float(message['joystick1'])*100)*powerP)) + " RightPower: " + str(int((float(message['joystick2'])*100)*powerP)))
    

@socketio.on('turret')
def my_event(message):
    #os.system('clear')
    #print(str(message))

    #Checks for shutdown
    shutdown = message['shutdown2']
    Shutdown(shutdown)

    Turret.start(int((float(message['turretControls'])*100)*0.3))
    Shoulder.start(int((float(message['shoulderControls'])*100)*powerT))
    Elbow.start(int((float(message['elbowControls'])*100)*powerT))
    Wrist.start(int((float(message['wristControls'])*100)*powerT))

    clawOpen = int(float(message['clawOpen'])*100)
    clawClose = int(float(message['clawClose'])*100)
    Claw.start(clawOpen - clawClose)

if __name__ == '__main__':
    print(Fore.RED + 'Server started' + Fore.RESET)
    socketio.run(app, debug=False, host='0.0.0.0')