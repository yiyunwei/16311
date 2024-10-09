from __future__ import print_function 
from __future__ import division
import brickpi3
import numpy as np
import math
import time

BP = brickpi3.BrickPi3()

leftmotor = BP.PORT_C
rightmotor = BP.PORT_D
maxpower = 25    

battery = BP.get_voltage_battery()
print(battery,"V\n")

startright = BP.get_motor_encoder(rightmotor)
startleft = BP.get_motor_encoder(leftmotor)

def test():
    try:
        start = time.time() 

        kp = 2
        BP.set_motor_power(rightmotor,maxpower)
        leftoffset = 0
        startright = BP.get_motor_encoder(rightmotor)
        startleft = BP.get_motor_encoder(leftmotor)
                                                                                                                                                                                                                                                                                                                
        while time.time()-start < 3:
            BP.set_motor_power(leftmotor,maxpower+kp*leftoffset)
        
            deltaright = startright-BP.get_motor_encoder(rightmotor)
            deltaleft = startleft-BP.get_motor_encoder(leftmotor)
            
            leftoffset = deltaright-deltaleft
            print(leftoffset)
            startright = BP.get_motor_encoder(rightmotor)
            startleft = BP.get_motor_encoder(leftmotor)

        BP.set_motor_power(leftmotor,0)
        BP.set_motor_power(rightmotor,0)

    except KeyboardInterrupt:
        BP.reset_all()
        BP.set_motor_power(leftmotor,0)
        BP.set_motor_power(rightmotor,0)

test()
