from flask import Flask, render_template
from flask_socketio import SocketIO, emit ## SocketIO is a python library that allows socket use for flask servers
from colorama import Fore ## Just so messages are different colors
from motorlib import *
import RPi.GPIO as GPIO

#Setup Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Setup Boards
io1 = board(0x18)
#io2 = board(0x19)

#Setup Motors
RightTread = motor(io1,pins = [1, 11]) ## In the order of (board, PWM pin, DIR pin)
FrontRightFlipper = motor(io1, pins = [3, 9])
BackRightFlipper = motor(io1, pins = [5, 7])

LeftTread = motor(io1, pins = [2, 12])
FrontLeftFlipper = motor(io1, pins = [4, 10])
BackLeftFlipper = motor(io1, pins = [6, 8])
"""
Turret = motor(io2, pins = [2, 10])

Shoulder = motor(io2, pins = [1, 9])

Elbow = motor(io2, pins = [5, 11])

Wrist = motor(io2, pins =[ 6, 12])

Claw = motor('pi', pins = [18, 23])
"""
#Setup Power Variables
# This can be changed to scale the power of the motors for the specific subsystems
powerDrive = 0.6
powerTurret = 0.25

def Shutdown(message):
    while message: ## check later for correct functionality
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
        print(Fore.RED + 'Shutdown' + Fore.RESET)

@app.route('/')
def index():
    return render_template('gamepad.html')

@socketio.on('connect')
def test_connect():
    print(Fore.GREEN + 'Client connected' + Fore.RESET)

@socketio.on('disconnect')
def test_disconnect():
    print(Fore.RED + 'Client disconnected' + Fore.RESET)

    #Stops all motors incase of disconnect
    ## fix later
    Shutdown(shutdown)

@socketio.on('treads')
def my_event(message):
    #os.system('clear')
    #print(str(message))

    #Checks for shutdown
    shutdown = message['shutdown']
    Shutdown(shutdown)

    LeftTread.start(int((float(message['joystick1'])*100)*powerDrive))
    RightTread.start(int((float(message['joystick2'])*100)*powerDrive))

    if (message['frontLeftFlipperUp']):
         print (message['frontLeftFlipperUp'])
         FrontLeftFlipper.start(50)
    elif (message['frontLeftFlipperDown']):
        FrontLeftFlipper.start(-50)  
    else:
        FrontLeftFlipper.start(0)

    if (message['frontRightFlipperUp']):
        FrontRightFlipper.start(-50)
    elif (message['frontRightFlipperDown']):
        FrontRightFlipper.start(50)
    else:
        FrontRightFlipper.start(0)
    
    if (message['backLeftFlipperUp']):
        BackLeftFlipper.start(50)
    elif (message['backLeftFlipperDown']):
        BackLeftFlipper.start(-50)
    else:
        BackLeftFlipper.start(0)
    if (message['backRightFlipperUp']):
        BackRightFlipper.start(50)
    elif (message['backRightFlipperDown']):
        BackRightFlipper.start(-50)
    else:
        BackRightFlipper.start(0)
    
    print("LeftPower: " + str(int((float(message['joystick1'])*100)*powerDrive)) + " RightPower: " + str(int((float(message['joystick2'])*100)*powerDrive)))
    

@socketio.on('turret')
def my_event(message):
    #os.system('clear')
    #print(str(message))

    #Checks for shutdown
    shutdown = message['shutdown2']
    Shutdown(shutdown)

    Turret.start(int((float(message['turretControls'])*100)*0.3))
    Shoulder.start(int((float(message['shoulderControls'])*100)*powerTurret))
    Elbow.start(int((float(message['elbowControls'])*100)*powerTurret))
    Wrist.start(int((float(message['wristControls'])*100)*powerTurret))

    clawOpen = int(float(message['clawOpen'])*100)
    clawClose = int(float(message['clawClose'])*100)
    Claw.start(clawOpen - clawClose)

if __name__ == '__main__':
    print(Fore.RED + 'Server started' + Fore.RESET)
    socketio.run(app, debug=False, host='0.0.0.0')