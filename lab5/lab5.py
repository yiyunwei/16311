"""
File:           lab5.py
Date:           2/15/2022
Description:    lab5 main starter code
Author:         Chi Gao (chig@andrew.cmu.edu)

"""

# import packages and files for helper functions 
from __future__ import print_function 
from __future__ import division
# from construct_map import construct_map
import brickpi3
import numpy as np
import math
import time

# import your odometry file HERE
from odometry import turn,getPosition
from construct_map import process_coords, construct_map

'''IMPORTANT NOTE: must run with python3 command for pathfinding to work'''

# create the Robot instance.
BP = brickpi3.BrickPi3()
# print(BP.get_voltage_battery(),"V\n")

DIAMETER = 2.24409449 #large grippy tires
RADIUS = DIAMETER/2
WHEELBASE = 3.75

# construct_map(starting x, starting y, goal x, goal y)
#commands = process_coords(construct_map(12, 30, 6, 6, 'easy'), 0)

theta = 0

def run_lines(commands):
    for c in commands:
        net_angle_turn, xi, yi, xf, yf = c
        #dist = math.sqrt((xf-xi)**2+(yf-yi)**2)
        #print(dist)
        _ = turn(net_angle_turn)
        getPosition(RADIUS, WHEELBASE,(0, xi, yi, xf, yf))

run_lines([])



# call helper functions from other files, such as:
# obstacle_map = construct_map()

# it is recommended to maintain modularity in this lab.
# your code will be more organized by creating several
# helper function files and importing functions.
