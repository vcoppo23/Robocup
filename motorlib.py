import ioexpander as io
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
io1 = io.IOE(i2c_addr=0x18) ## This is the address of the first expander board
io2 = io.IOE(i2c_addr=0x19) ## This is the address of the second expander board
####
# To change an expander board's address, use the following command:
# just open a python3 shell while using the pi with $ python3
# then copy this $ "import ioexpander"
# then $ "io1.set_i2c_addr(desired_address)" the desired address must be in the form of 0x## where # is the readout when you use the command i2cdetect -y 1
# this will permantly change the address of the expander board until you change it again. It will not change even if it is powered off
####
frequency = 1000 ##This is the frequency of the pwm signal for the expander boards
div = 128 ##This is the divider for the pwm signal for the expander boards
period = int(24000000/div/frequency)
##The following four lines dial in the frequency of the pwm signal to 1000hz, which reduces stutter and rumble
##This needs to be further looked into as it drains the power faster than the default 100hz on the pi itself
io1.set_pwm_control(divider=div) 
io1.set_pwm_period(period)
io2.set_pwm_control(divider=div)
io2.set_pwm_period(period)


objectlist = [] ##This is a list of all the motors that are created



class motor:
    def __init__(self,board, pwm, DIR): ## Create a motor by giving it a board, pwm pin, and direction pin. The Board options are "pi", "io1", and "io2"
        self.board = board
        self.pwm = pwm
        self.DIR = DIR #capatilized to avoid conflict with the dir() function
        objectlist.append(self) ##This adds the motor to the list of motors

        if board == "pi": ##This sets up the motor if it attatchd to the pi directly
            GPIO.setup(pwm,GPIO.OUT)
            GPIO.setup(DIR,GPIO.OUT)
            self.object = GPIO.PWM(pwm,100)

        if board == "io1": ##This sets up the motor if it attatched to io expander 1
            io1.set_mode(pwm, io.PWM)
            io1.set_mode(DIR, io.PIN_MODE_PP)

        
        if board == "io2": ##This sets up the motor if it attatched to io expander 2
            io2.set_mode(pwm, io.PWM)
            io2.set_mode(DIR, io.PIN_MODE_PP)

    def start(self,speed): ##Start the motor by giving it a speed, direction is determined by the sign of the speed (range from -100 to 100)

        if self.board == "pi":
            scaled_speed = int((period/100)*speed) ##This scales the speed to the period of the pwm signal 

            if speed > 0:
                GPIO.output(self.DIR,GPIO.HIGH)
                self.object.start(speed)
            elif speed < 0 and speed >= -100:
                GPIO.output(self.DIR,GPIO.LOW)
                self.object.start(-speed)

        if self.board == "io1": 
            if speed > 0 and speed <= 100:
                io1.output(self.DIR,1)
                io1.output(self.pwm,scaled_speed)
            elif speed < 0 and speed >= -100:
                io1.output(self.DIR,0)
                io1.output(self.pwm,-scaled_speed)
        
        if self.board == "io2": 
            if speed > 0 and speed <= 100:
                io2.output(self.DIR,1)
                io2.output(self.pwm,scaled_speed)
            elif speed < 0 and speed >= -100:
                io2.output(self.DIR,0)
                io2.output(self.pwm,-scaled_speed)

        def stop(self):
            if self.board == "pi":
                self.object.stop()
            if self.board == "io1":
                io1.output(self.pwm,0)
                io1.output(self.DIR,0)
            if self.board == "io2":
                io2.output(self.pwm,0)
                io2.output(self.DIR,0)
        
def stopall():
    for i in objectlist:
        i.stop()

##Example of how to use this class

shoulder = motor("io1",1,3) ##Create a motor object for the shoulder motor
shoulder.start(50) ##Start the shoulder motor at 50% speed






        

