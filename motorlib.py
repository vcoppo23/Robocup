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
# then copy this $ "import ioexpander"
# then $ "io1.set_i2c_addr(desired_address)" the desired address must be in the form of 0x## where # is the readout when you use the command i2cdetect -y 1
# this will permantly change the address of the expander board until you change it again. It will not change even if it is powered off
####
frequency = 1000 ##This is the frequency of the pwm signal for the expander boards
div = 128 ##This is the divider for the pwm signal for the expander boards
period = int(24000000/div/frequency)

objectlist = [] ##This is a list of all the motors that are created

class board(): ##Creates a board class

    def __init__(self, hex_address, type = "expander"): ##This is a function to set up the expander boards
        self.address = io.IOE(i2c_addr=hex_address) 
        self.type = type ##This is the type of board, either "pi" or "expander"
    def get_board_type(self):
        print (self.board_type)

    def get_address(self):
        print ("The current address of this board is: " + self.hex_address)


class motor:

    def __init__(self,board, pwm, DIR): ## Create a motor by giving it a board, pwm pin, and direction pin
        self.board = board ## The Board options are "pi", "io1", and "io2"
        self.pwm = pwm ## pwm pin, controls motor speed
        self.DIR = DIR ##direction pin, capatilized to avoid conflict with the dir() function
        self.lastspeed = 0  ##This is used to track the most recent speed of the motor for the stepper function
        objectlist.append(self) ##This adds the motor to the list of motor objects
        

        if board == "pi": ##This sets up the motor if it is attatchd to the pi directly
            GPIO.setup(pwm,GPIO.OUT)
            GPIO.setup(DIR,GPIO.OUT)
            self.object = GPIO.PWM(pwm,100)

        if board.type == "expander": ##This sets up the motor if it is attatched to io expander 1
            board.address.set_mode(pwm, io.PWM)
            board.address.set_mode(DIR, io.PIN_MODE_PP)
            

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

        if self.board.type == "expander": 
            if speed == 0:
                board.address.set_pwm_control(divider=div) 
                board.address.set_pwm_period(period)
                board.address.output(self.pwm,0)
                board.address.output(self.DIR,0)

            elif speed > 0:
                ## The following two lines dial in the frequency of the pwm signal to 1000hz, which reduces stutter and rumble
                ## This needs to be further looked into as it drains the power faster than the default 100hz on the pi itself
                ## It is necessary to set the pwm period and divider for the expander boards when starting the motor for unknown reasons
                board.address.set_pwm_control(divider=div) 
                board.address.set_pwm_period(period)
                board.address.output(self.DIR,1)
                board.address.output(self.pwm,scaled_speed)

            elif speed < 0:
                board.address.set_pwm_control(divider=div) 
                board.address.set_pwm_period(period)
                board.address.output(self.DIR,0)
                board.address.output(self.pwm,-scaled_speed)
        
    def stop(self):
        self.lastspeed = 0 ##This sets the last known speed to 0 
        if self.board == "pi":
            self.object.stop()
        if self.board.type == "expander":

            board.address.output(self.pwm,0)
            board.address.output(self.DIR,0)
        
def stopall():
    for i in objectlist:
        i.stop()

def shutdown(): ## This function can be called as an emergency stop, it will stop all motors and then shut down the pi
    stopall()
    GPIO.cleanup()
    
    call("sudo shutdown -h now", shell=True)





        

