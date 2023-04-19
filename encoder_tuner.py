import keyboard 
import motorlib
import time
slices = 10
speedlist = []
def tune_encoder(vroom):
    print(vroom.pins)
    if vroom.encoder == None:
        print ("This motor does not have an encoder attatched")
        return

    for i in range(0,slices):

        while keyboard.is_pressed('q') == False:
            vroom.start(i*10)
            angle = vroom.get_angle()
            print (angle)
        else:
            vroom.stop()
            speedlist.append(angle)
            time.sleep(2)

    print (speedlist)




        
