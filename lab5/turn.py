# import packages and files for helper functions 
from __future__ import print_function 
from __future__ import division
import brickpi3
import numpy as np
import math
import time
def turn(angle):

    if angle==-45:
        BP.set_motor_dps(leftmotor, 45)
        BP.set_motor_dps(rightmotor,-50)
        start_Time = time.time()
        time.sleep(0.01)
        end_Time = time.time()
        while end_Time - start_Time < 2:
            end_Time = time.time()
    
    elif angle==45:
        BP.set_motor_dps(leftmotor, -50)
        BP.set_motor_dps(rightmotor, 45)

        start_Time = time.time()
        time.sleep(0.01)
        end_Time = time.time()
        while end_Time - start_Time < 2:
            end_Time = time.time()

    elif angle==90:
        BP.set_motor_dps(leftmotor, -100)
        BP.set_motor_dps(rightmotor, 90)

        start_Time = time.time()
        time.sleep(0.01)
        end_Time = time.time()
        while end_Time - start_Time < 2:
            end_Time = time.time()

    elif angle==-90:
        BP.set_motor_dps(leftmotor, 90)
        BP.set_motor_dps(rightmotor, -90)

        start_Time = time.time()
        time.sleep(0.01)
        end_Time = time.time()
        while end_Time - start_Time < 2:
            end_Time = time.time()

    elif angle==135:
        BP.set_motor_dps(leftmotor, -140)
        BP.set_motor_dps(rightmotor, 135)

        start_Time = time.time()
        time.sleep(0.01)
        end_Time = time.time()
        while end_Time - start_Time < 2:
            end_Time = time.time()

    elif angle==-135:
        BP.set_motor_dps(leftmotor, 135)
        BP.set_motor_dps(rightmotor, -135)

        start_Time = time.time()
        time.sleep(0.01)
        end_Time = time.time()
        while end_Time - start_Time < 2:
            end_Time = time.time()


    BP.set_motor_power(leftmotor,0)
    BP.set_motor_power(rightmotor,0)
    return None