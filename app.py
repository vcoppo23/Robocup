from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from colorama import Fore
from motorlib import *
import RPi.GPIO as GPIO
import cv2


#Setup Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Setup Motors
RightTread = motor("pi", 1, 9)
FrontRightFlipper = motor("pi", 3, 11)
BackRightFlipper = motor("pi", 4, 13)

LeftTread = motor("pi", 2, 10)
FrontLeftFlipper = motor("pi", 5, 12)
BackLeftFlipper = motor("pi", 3, 14)

Turret = motor("pi", 1, 10)

Shoulder = motor("pi", 2, 9)

Elbow = motor("pi", 6, 13)

Wrist = motor("pi", 4, 14)

Claw = motor("pi", 1, 9)

#Setup Power Variables
powerP = 0.6
powerT = 0.6

def Shutdown(message):
    while message == "true":
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

    if (message['frontLeftFlipperUp'] == 'true'):
         FrontLeftFlipper.start(50)
    elif (message['frontLeftFlipperDown'] == 'true'):
        FrontLeftFlipper.start(-50)  
    else:
        FrontLeftFlipper.start(0)

    if (message['frontRightFlipperUp'] == 'true'):
        FrontRightFlipper.start(-50)
    elif (message['frontRightFlipperDown'] == 'true'):
        FrontRightFlipper.start(50)
    else:
        FrontRightFlipper.start(0)
    
    if (message['backLeftFlipperUp'] == 'true'):
        BackLeftFlipper.start(50)
    elif (message['backLeftFlipperDown'] == 'true'):
        BackLeftFlipper.start(-50)
    else:
        BackLeftFlipper.start(0)
    if (message['backRightFlipperUp'] == 'true'):
        BackRightFlipper.start(50)
    elif (message['backRightFlipperDown'] == 'true'):
        BackRightFlipper.start(-50)
    else:
        BackRightFlipper.start(0)
    
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

claw_cam = 0
front_left = 1
front_right = 2
back = 3

def get_frame(cam_num, claw):
    #set video capture device with device number, variables above
    camera = cv2.VideoCapture(cam_num)

    #camera width
    w=320
    #camera height
    h=240

    camera.set(3,w)
    camera.set(4,h)
    camera.set(cv2.CAP_PROP_FPS, 20)


    while True:
        ret, frame = camera.read()
        if not ret:
            break
        if not claw:
            alpha = 30
            beta = 1
            #sets frame to black and white if not claw camera
            newFrame = cv2.convertScaleAbs(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), alpha, beta)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', newFrame)[1].tobytes() + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n\r\n')
            
@app.route('/video_feed0')
def video_feed0():
    return Response(get_frame(claw_cam, True), mimetype='multipart/x-mixed-replace; boundary=frame')

#Route to front left camera
@app.route('/video_feed1')
def video_feed1():
    return Response(get_frame(front_left, False), mimetype='multipart/x-mixed-replace; boundary=frame')

#Route to front right camera
@app.route('/video_feed2')
def video_feed2():
    return Response(get_frame(front_right, False), mimetype='multipart/x-mixed-replace; boundary=frame')

#Route to back camera
@app.route('/video_feed3')
def video_feed3():
    return Response(get_frame(back, False), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print(Fore.RED + 'Server started' + Fore.RESET)
    socketio.run(app, debug=False, host='0.0.0.0')