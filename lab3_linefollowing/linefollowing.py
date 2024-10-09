from __future__ import print_function
from __future__ import division

import time
import brickpi3

BP = brickpi3.BrickPi3()

lightport = BP.PORT_4
rightmotor = BP.PORT_D
leftmotor = BP.PORT_A
direction = 0

BP.set_sensor_type(lightport, BP.SENSOR_TYPE.NXT_LIGHT_ON)

try:
    rpower = 27
    lpower = 27
    BP.set_motor_power(rightmotor, rpower)
    BP.set_motor_power(leftmotor, lpower)
    
    seenblack = True
    while True:
        try:
            value = BP.get_sensor(lightport)
            #print(value)
            
            if (value < 2000 and seenblack):# threshold for sensing (white?)
                if direction==-1:
                    direction = 1
                    rpower = 22
                    lpower = -25
                elif direction==1:
                    direction = -1
                    rpower = -25 # can adjust power values to go faster or slower
                    lpower = 22
                seenblack = False
                #time.sleep(0.5)
                #print("right turn ", value)
            elif value < 2000:
                direction = -1
                rpower = 22
                lpower = -25
            elif value > 2300:
                direction = 1
                rpower = -25
                lpower = 22
                seenblack = True
                #time.sleep(0.5)
                #seenback = False
                #print("left turn ", value)
            else:
                rpower = 27
                lpower = 27
            #direction = direction * -1
            BP.set_motor_power(rightmotor, rpower)
            BP.set_motor_power(leftmotor, lpower)
            #else:
                #seenblack = True
                #time.sleep(0.5)
            
        except brickpi3.SensorError as error:
            print(error)
            rpower = 0
            lpower = 0
            
        time.sleep(0.03) # delay between measurements
    
except KeyboardInterrupt:
    BP.set_motor_power(leftmotor,0)
    BP.set_motor_power(rightmotor,0)
    BP.reset_all()