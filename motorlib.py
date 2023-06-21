# Robocup'23 - Motor Library
# BSM Robotics
# Val Coppo

import ioexpander as io ## install with $ pip3 install pimoroni-ioexpander
import RPi.GPIO as GPIO
import time
from encoder import Encoder
from subprocess import call
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
####
# To change an expander board's address, use the following command:
# open a python3 shell while using the pi and the board is plugged in with $ python3
# then copy this $ "import ioexpander as io"
# then type in "io1 = io.IOE(i2c_addr=0x18)"
# then $ "io1.set_i2c_addr(desired_address)" the desired address must be in the form of 0x## where # is the readout when you use the command i2cdetect -y 1
# this will permantly change the address of the expander board until you change it again. It will not change even if it is powered off
####
frequency = 1000 ##This is the frequency of the pwm signal for the expander boards
div = 128 ##This is the divider for the pwm signal for the expander boards
period = int(24000000/div/frequency)
encoder_tune = 7 ##This is a tuning factor for the encoders, experimental derived value
objectlist = [] ##This is a list of all the motors that are created

class board(): ##Creates a board class

    def __init__(self, hex_address, type = "expander"): ##This is a function to set up the expander boards
        self.type = type ##This is the type of board, either "pi" or "expander"

        if hex_address != "pi": ##This sets up the board if it is attatched to the pi directly
            self.address = io.IOE(i2c_addr=hex_address) 
        else:
            self.address = "pi"

    def get_address(self): ##This is a function to get the address of the board
        return self.address
    def get_type(self):
        return self.type

class motor:

    def __init__(self,board, pins = None, encoder = None, gear_ratio = None): ## Create a motor by giving it a board, pwm pin, and direction pin
        self.board = board ## The Board options are "pi", "io1", and "io2"
        self.pins = pins ## The pins are in the order of [pwm, dir]
        if len(pins) != 2:
            print ("motor needs 2 pins")
            return
        
        self.pwm = pins[0] ## pwm pin, controls motor speed
        self.DIR = pins[1] ##direction pin, capatilized to avoid conflict with the dir() function
        self.lastspeed = 0  ##This is used to track the most recent speed of the motor for the stepper function
        self.gear_ratio = gear_ratio ##This is the gear ratio of the motor
        if encoder != None:
            if len(encoder) != 2:
                print ("encoder needs 2 pins")
                return
            else:
                self.encdoder = Encoder(encoder[0],encoder[1])
        
         ##This is the encoder object that is attatched to the motor
        objectlist.append(self) ##This adds the motor to the list of motor objects
        

        if self.board.type == "pi": ##This sets up the motor if it is attatchd to the pi directly
            GPIO.setup(self.pwm,GPIO.OUT)
            GPIO.setup(self.DIR,GPIO.OUT)
            self.object = GPIO.PWM(self.pwm,100)

        elif self.board.type == "expander": ##This sets up the motor if it is attatched to io expander 1
            self.board.address.set_mode(self.pwm, io.PWM)
            self.board.address.set_mode(self.DIR, io.PIN_MODE_PP)
        else:
            print ("Board not found")

    def start(self,speed): ##Start the motor by giving it a speed, direction is determined by the sign of the speed (range from -100 to 100)
        scaled_speed = int((period/100)*speed) ##This scales the speed to the period of the pwm signal 
        self.lastspeed = speed
        
        if speed > 100 or speed < -100:
            print ("Speed out of range: must be between -100 and 100")
            return
        
        if self.board == "pi":
            
            ## the speed must be scaled becuase the pwm period is different for the expanders, this normalizes the speed for all inputs
            if speed == 0:
                self.object.stop()
            elif speed > 5:
                GPIO.output(self.DIR,GPIO.HIGH)
                self.object.start(speed)
            elif speed < -5:
                GPIO.output(self.DIR,GPIO.LOW)
                self.object.start(-speed)

        if self.board.get_type() == "expander": 
            if speed == 0:
                self.board.address.set_pwm_control(divider=div) 
                self.board.address.set_pwm_period(period)
                self.board.address.output(self.pwm,0)
                self.board.address.output(self.DIR,0)

            elif speed > 0:
                ## The following two lines dial in the frequency of the pwm signal to 1000hz, which reduces stutter and rumble
                ## This needs to be further looked into as it drains the power faster than the default 100hz on the pi itself
                ## It is necessary to set the pwm period and divider for the expander boards when starting the motor for unknown reasons
                self.board.address.set_pwm_control(divider=div) 
                self.board.address.set_pwm_period(period)
                self.board.address.output(self.DIR,1)
                self.board.address.output(self.pwm,scaled_speed)

            elif speed < 0:
                self.board.address.set_pwm_control(divider=div) 
                self.board.address.set_pwm_period(period)
                self.board.address.output(self.DIR,0)
                self.board.address.output(self.pwm,-scaled_speed)
    
        
    def stop(self):
        self.lastspeed = 0 ##This sets the last known speed to 0 
        if self.board == "pi":
            self.object.stop()
        if self.board.type == "expander":

            self.board.address.output(self.pwm,0)
            self.board.address.output(self.DIR,0)


    def get_angle(self):
        if self.encoder != None:
            return (self.encoder.getValue()*360)/(encoder_tune * self.gear_ratio)
        else:
            print ("This motor does not have an encoder attatched")
        
def stopall():
    for i in objectlist:
        i.stop()

def shutdown(): ## This function can be called as an emergency stop, it will stop all motors and then shut down the pi
    stopall()
    GPIO.cleanup()
    
    call("sudo shutdown -h now", shell=True)



