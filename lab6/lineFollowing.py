from __future__ import print_function 
from __future__ import division
import numpy as np
import math, time, brickpi3

'''
    Lab 6: Localization
'''

#2400 = on the line, 1800 = off the line
LEFT = -1
RIGHT = 1

BP = brickpi3.BrickPi3()
print(BP.get_voltage_battery())
leftmotor = BP.PORT_A
rightmotor = BP.PORT_D
lightport = BP.PORT_4
BP.set_sensor_type(lightport, BP.SENSOR_TYPE.NXT_LIGHT_ON)
time.sleep(3) #need delay after initializing so that sensor readings don't break

BP.set_motor_power(rightmotor, 0)
BP.set_motor_power(leftmotor, 0)



def followLine(SPEED, maptype):

    while True:
        try:
            try:
                value = BP.get_sensor(lightport)  
                lpower = SPEED
                R_SPEED = SPEED*-0.67
                L_SPEED = SPEED*1.1


                if value < 1800: # on white
                    rpower = SPEED
                    lpower = SPEED
                elif value>2100: # fully on black
                    rpower = -1*SPEED
                    lpower = SPEED
                else: # default value (on circle's inside edge)
                    rpower = R_SPEED
                    lpower = L_SPEED


                BP.set_motor_power(rightmotor, rpower) 
                BP.set_motor_power(leftmotor, lpower)               
               
            except brickpi3.SensorError as error:
                print(error)
                BP.set_motor_power(leftmotor,0)
                BP.set_motor_power(rightmotor,0)
                BP.reset_all()

        except KeyboardInterrupt:
            BP.set_motor_power(leftmotor,0)
            BP.set_motor_power(rightmotor,0)
            BP.reset_all()


#followLine(25, "challenge")