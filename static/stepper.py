

def stepper (current_speed,goal_speed,steps = 5):
   
   speedlist = []
   if -100 > goal_speed > 100:
      return
   if current_speed < goal_speed:
      for i in range(current_speed, goal_speed+1, (goal_speed-current_speed)//steps):
         speedlist.append(i)
   elif goal_speed < current_speed:
      for i in reversed(range(goal_speed, current_speed+1, (current_speed-goal_speed)//steps)):    
         speedlist.append(i)
   current_speed = goal_speed
   return speedlist


