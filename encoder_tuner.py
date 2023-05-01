
from  motorlib import *
import time
def tune_encoder(vroom):
    rotatations = input(int("How many rotations: "))
    gear_ratio = input(int("Gear ratio: "))
    speed = input(int("speed: "))
    end_value = (encoder.getValue()*360)/(7 * gear_ratio)
    vroom.start(speed)
    




        
