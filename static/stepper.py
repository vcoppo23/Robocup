current_speed = 0
def stepper (speed):
   speedlist = []
   if -100 > speed > 100:
      print ("don't fry the motors")
      return
   print ('speed at: ' + str(current_speed) + '%')
   if current_speed < speed:
      for i in range(current_speed, speed+1, (speed-current_speed)//5):
         speedlist.append(i)
         print ('speed: ' +str(i)+ '%')
   elif speed < current_speed:
      for i in reversed(range(speed, current_speed+1, (current_speed-speed)//5)):    
         speedlist.append(i)
         print ('speed: ' +str(i)+ '%')
   current_speed = speed
   return speedlist