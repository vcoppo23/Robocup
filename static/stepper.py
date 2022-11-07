global curret_speed

def stepper (speed):
   speedlist = []
   if -100 > speed > 100:
      return
   if current_speed < speed:
      for i in range(current_speed, speed+1, (speed-current_speed)//5):
         speedlist.append(i)
   elif speed < current_speed:
      for i in reversed(range(speed, current_speed+1, (current_speed-speed)//5)):    
         speedlist.append(i)
   current_speed = speed
   return speedlist