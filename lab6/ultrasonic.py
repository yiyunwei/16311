from __future__ import print_function 
from __future__ import division
import numpy as np
import math, time, brickpi3

'''
    Lab 6: Localization
'''

#initializing brick
BP = brickpi3.BrickPi3()
print(BP.get_voltage_battery())

leftmotor = BP.PORT_A
rightmotor = BP.PORT_D
ultrasonic = BP.PORT_4
BP.set_sensor_type(ultrasonic, BP.SENSOR_TYPE.NXT_ULTRASONIC)

time.sleep(3)

while True:
    try:
        value = BP.get_sensor(ultrasonic)
        print(value)
        time.sleep(0.1)
    except KeyboardInterrupt:
        BP.reset_all()