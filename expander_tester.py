import ioexpander as io ## install with $ pip3 install pimoroni-ioexpander
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
io1 = io.IOE(i2c_addr=0x18)
frequency = 1000 ##This is the frequency of the pwm signal for the expander boards
div = 128 ##This is the divider for the pwm signal for the expander boards
period = int(24000000/div/frequency)
for pin in range(1,15):
    print(pin)
    if pin < 6:
        io1.set_mode(pin, io.PWM)
        io1.set_pwm_control(divider=div) 
        io1.set_pwm_period(period)
        io1.output(pin,int((period/100)*100))
        time.sleep(5)
        io1.output(pin,0)
    else:
        io1.set_mode(pin, io.PIN_MODE_PP)
        io1.output(pin,1)
        time.sleep(5)
        io1.output(pin,0)
    