from __future__ import print_function 
from __future__ import division
import numpy as np
import math, time, brickpi3

import map

'''
    Lab 6: Localization
'''
#robot constants
DIAMETER = 2.24409449 #large grippy tires
RADIUS = DIAMETER/2
WHEELBASE = 7.5

#initializing brick
BP = brickpi3.BrickPi3()
print(BP.get_voltage_battery())

leftmotor = BP.PORT_A
rightmotor = BP.PORT_D
ultrasonic = BP.PORT_1
BP.set_sensor_type(ultrasonic, BP.SENSOR_TYPE.NXT_ULTRASONIC)

#2400 = on the line, 1800 = off the line
LEFT = -1
RIGHT = 1
lightport = BP.PORT_4
BP.set_sensor_type(lightport, BP.SENSOR_TYPE.NXT_LIGHT_ON)

time.sleep(3) #need delay after initializing so that sensor readings don't break

BP.set_motor_power(rightmotor, 0)
BP.set_motor_power(leftmotor, 0)

    #main loop
while (True):
    SPEED = 20
    try:
        value = BP.get_sensor(lightport)
        #print(value)

        rpower = SPEED*0.75
        lpower = SPEED*1.5

        if value < 1800: # on white
            rpower = SPEED*0.4
            lpower = SPEED*1.8

        #elif value>2100: # fully on black
        #    rpower = -0.7*SPEED
        #    lpower = 1.1*SPEED
            ##print(value)
        else:
            #print("default case")
            rpower = SPEED*0.75
            lpower = SPEED*1.5

        BP.set_motor_power(rightmotor, rpower) 
        BP.set_motor_power(leftmotor, lpower) 

    except KeyboardInterrupt:
        BP.set_motor_power(leftmotor, 0)
        BP.set_motor_power(rightmotor, 0)
        BP.reset_all()
        break


c_map=[0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0] #TA given map of obstacles
goal_state=0
    
localization("", c_map, goal_state)