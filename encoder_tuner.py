import keyboard 
import motorlib
import time
slices = 10
speedlist = []
def tune_encoder(motor):
    if motor.encoder == None:
        print ("This motor does not have an encoder attatched")
        return

    for i in range(0,slices):

        while keyboard.is_pressed('q') == False:
            motor.start(i*10)
            angle = motor.get_angle()
            print (angle)
        else:
            motor.stop()
            speedlist.append(angle)
            time.sleep(2)

    print (speedlist)




        
