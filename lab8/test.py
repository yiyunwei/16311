from __future__ import print_function
from __future__ import division

import time
import brickpi3

BP = brickpi3.BrickPi3()
print(BP.get_voltage_battery(),"V\n")

rightmotor = BP.PORT_C
leftmotor = BP.PORT_D

#runtime = 30
#15 = 18.8, 20 = 25.5, 25 = 32.75, 30 = 38, 35 = 44.5

def walk_dist(x):


    #runtime = round(-0.000809301*(x**2)+0.832783*x+0.665159)
    runtime = round(-0.000423717*(x**2)+0.63195*x+1.90663)
    #1.90663

    
    try:
        
        
        starttime = time.time()
        rpower = 40
        lpower = 40
        BP.set_motor_power(rightmotor, rpower)
        BP.set_motor_power(leftmotor, lpower)
        while(time.time()-starttime < runtime):
            #nothing
            hi=0
        
        BP.set_motor_power(rightmotor, 0)
        BP.set_motor_power(leftmotor, 0)
        return

    except KeyboardInterrupt:
        BP.set_motor_power(leftmotor, 0)
        BP.set_motor_power(rightmotor, 0)
        BP.reset_all()
        return
        

walk_dist(55)