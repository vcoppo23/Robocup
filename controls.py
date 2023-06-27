import pygame
#import Rpi.GPIO as GPIO
#from motorlib import *
from time import sleep

#Setup Boards
"""io1 = board(0x18)
io2 = board(0x19)
pi = board('pi',type = "pi")"""

#Setup Motors
"""RightTread = motor(pi,pins = [1, 11])  In the order of (board, PWM pin, DIR pin)
FrontRightFlipper = motor(io1, pins = [3, 9])
BackRightFlipper = motor(io1, pins = [5, 7])

LeftTread = motor(pi, pins = [2, 12])
FrontLeftFlipper = motor(io1, pins = [4, 10])
BackLeftFlipper = motor(io1, pins = [6, 8])

Turret = motor(io2, pins = [2, 12])

Shoulder = motor(io2, pins = [1, 11])

Elbow = motor(io2, pins = [3, 9])

Wrist = motor(io2, pins =[ 4, 10])

Forearm = motor('io2', pins = [5, 7])

Claw = motor('pi', pins = [6, 8])"""

#Setup Power Variables
#This can be changed to scale the power of the motors for the specific subsystems
powerDrive = 0.6
powerTurret = 0.25

#create pygame window
pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Robocup')

#put a big red circle in the center of the screen
pygame.draw.circle(screen, (255, 0, 0), (320, 240), 150)

#show the pygame window
pygame.display.flip()

#Set mode
#0 = tread, 1 = turret
mode = 0

joystick = pygame.joystick.Joystick(0)  # Use index 0 for the first joystick
joystick.init()
#axis 0 = left stick x
#axis 1 = left stick y
#axis 2 = right stick x
#axis 3 = right stick y

def treadControl():
    #Tread Control
    #LeftTread.start(powerDrive * int(joystick.get_axis(1)*100))
    #RightTread.start(powerDrive * int(joystick.get_axis(3)*100))
    #print("Left Tread: " + str(int(joystick.get_axis(1)*100)) + " Right Tread: " + str(int(joystick.get_axis(3)*100)))

    #FLipper Control
    left_dpad = joystick.get_button(7)
    right_dpad = joystick.get_button(5)
    up_dpad = joystick.get_button(4)
    down_dpad = joystick.get_button(6)

    print("Left Dpad: " + str(left_dpad) + " Right Dpad: " + str(right_dpad) + " Up Dpad: " + str(up_dpad) + " Down Dpad: " + str(down_dpad))



def turretControl():
    global mode
    pass






#run until the user asks to quit
running = True
while running:
    #did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #check if big red circle was clicked
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if 170 < pos[0] < 470 and 90 < pos[1] < 390:
            print('Shutting down...')
            running = False
    treadControl()
    sleep(0.5)

    