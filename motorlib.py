import ioexpander as io ## install with $ pip3 install pimoroni-ioexpander
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
io1 = io.IOE(i2c_addr=0x18) ## This is the address of the first expander board
io2 = io.IOE(i2c_addr=0x19) ## This is the address of the second expander board
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

        if board == "io1": ##This sets up the motor if it is attatched to io expander 1
            io1.set_mode(pwm, io.PWM)
            io1.set_mode(DIR, io.PIN_MODE_PP)
            
        if board == "io2": ##This sets up the motor if it is attatched to io expander 2
            io2.set_mode(pwm, io.PWM)
            io2.set_mode(DIR, io.PIN_MODE_PP)

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

        if self.board == "io1": 
            if speed == 0:
                io1.set_pwm_control(divider=div) 
                io1.set_pwm_period(period)
                io1.output(self.pwm,0)
                io1.output(self.DIR,0)

            elif speed > 0:
                ## The following two lines dial in the frequency of the pwm signal to 1000hz, which reduces stutter and rumble
                ## This needs to be further looked into as it drains the power faster than the default 100hz on the pi itself
                ## It is necessary to set the pwm period and divider for the expander boards when starting the motor for unknown reasons
                io1.set_pwm_control(divider=div) 
                io1.set_pwm_period(period)
                io1.output(self.DIR,1)
                io1.output(self.pwm,scaled_speed)

            elif speed < 0:
                io1.set_pwm_control(divider=div) 
                io1.set_pwm_period(period)
                io1.output(self.DIR,0)
                io1.output(self.pwm,-scaled_speed)
        
        if self.board == "io2": 
            if speed == 0:
                io2.set_pwm_control(divider=div)
                io2.set_pwm_period(period)
                io2.output(self.pwm,0)
                io2.output(self.DIR,0)

            elif speed > 0:
                io2.set_pwm_control(divider=div)
                io2.set_pwm_period(period)
                io2.output(self.DIR,1)
                io2.output(self.pwm,scaled_speed)
                
            elif speed < 0:
                io2.set_pwm_control(divider=div)
                io2.set_pwm_period(period)
                io2.output(self.DIR,0)
                io2.output(self.pwm,-scaled_speed)

    def stop(self):
        self.lastspeed = 0 ##This sets the last known speed to 0 
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

def shutdown(): ## This function can be called as an emergency stop, it will stop all motors and then shut down the pi
    GPIO.cleanup()
    from subprocess import call
    call("sudo shutdown -h now", shell=True)





        

