from __future__ import print_function 
from __future__ import division
import numpy as np
import math, time, brickpi3

'''
    Lab 6: Localization
'''

BP = brickpi3.BrickPi3()
# print(BP.get_voltage_battery(),"V\n")

leftmotor = BP.PORT_A
rightmotor = BP.PORT_D
