from re import U
from flask import Flask, render_template, Response, request
from time import sleep
from static.encoder import Encoder
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# This is designed to test half of the chasis, including the one motor running the tread and the two flippers
#Setup for Tread
AN1 = 22
DIG1 = 27
GPIO.setup(AN1, GPIO.OUT)
GPIO.setup(DIG1, GPIO.OUT)
p1 = GPIO.PWM(AN1, 100)


#Setup for Flippers
AN3 = 19
AN2 = 16
DIG3 = 26
DIG2 = 20
GPIO.setup(AN3, GPIO.OUT)
GPIO.setup(AN2, GPIO.OUT)
GPIO.setup(DIG3, GPIO.OUT)
GPIO.setup(DIG2, GPIO.OUT)
p2 = GPIO.PWM(AN2, 100)
p3 = GPIO.PWM(AN3, 100)

# Setup for Encoders
encoder1 = Encoder(17, 4)
encoder2 = Encoder(10, 9)

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
      leftTrigger = request.form['leftTrigger']
      rightTrigger = request.form['rightTrigger']
      xbutton = request.form['xbutton']

      leftTrigger = (int(float(leftTrigger)*100))//4
      rightTrigger = (int(float(rightTrigger)*100))//4
      joystick1 = (int((float(joystick1)*100)))//4
      joystick2 = (int((float(joystick2)*100)))//4 
      
      

      
      
      
      e1postition = ((((encoder1.getValue())/1350)*360)//1)
      e2postition = ((((encoder2.getValue())/1350)*360)//1)
      #Tread
      if leftTrigger > 0:
         
         GPIO.output(DIG1, GPIO.HIGH)
         p1.start(leftTrigger)

      elif rightTrigger > 0:
         
         GPIO.output(DIG1, GPIO.LOW)
         p1.start(rightTrigger)
      


         
      #Flippers
      if joystick1 < 0:
         print(e1postition)
         
         GPIO.output(DIG2, GPIO.HIGH)
         GPIO.output(DIG3, GPIO.HIGH)
         p3.start(-joystick1)
         

      elif joystick1 > 0:
         print(e1postition)
         GPIO.output(DIG2, GPIO.LOW)
         GPIO.output(DIG3, GPIO.LOW)
         p3.start(joystick1)
         



      
      
   return render_template('gamepad.html')

if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True, threaded=True)