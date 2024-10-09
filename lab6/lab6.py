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

def localization(maptype, curr_map, goal):
    #initializing variables
    sect_dist=4.75 #in inches, straight line distance
    avg_sensor_dist=0 #average value read by ultrasonic
    samples=[] #distance samples from current section
    curr_dist=0 #distance traveled since section start

    #range for ultrasonic: 
    lower_bound=13
    upper_bound=39
    total_dist=0
    obs=[] #obstacle array
    multiplier=1

    if(maptype == "challenge"):
        difficulty = True
        multiplier=0.95
    else:
        difficulty = False
    
    currInfo = [] #array with probability of starting location
    for i in range(len(curr_map)):
        currInfo += [1/len(curr_map)]
    p_map=map.getProbMap(curr_map, difficulty)

    #odometry initializations
    start_time = time.time()
    start_left = BP.get_motor_encoder(BP.PORT_A) #degrees
    start_right = BP.get_motor_encoder(BP.PORT_D) #degrees
    SPEED=20
    old_t=0
    seenBlock = False

    #main loop
    while (True):
        #line following goes here
        #need to save power values for later

        try:
        
            value = BP.get_sensor(lightport)

            lpower = SPEED
            if maptype=="regular":
                R_SPEED = SPEED*0.75 #-0.67
                L_SPEED = SPEED*1.7 #1.5
            else:
                R_SPEED = SPEED*0.75
                L_SPEED = SPEED*1.7

            rpower = SPEED*0.7
            lpower = SPEED*1.2


            if (value < 1750 and maptype=="regular"):
                rpower = SPEED*0.7 #0.8
                lpower = SPEED #0.8

            '''elif  (maptype=="challenge" and value < 1750): # on white
                rpower = SPEED*0.7 #0.8
                lpower = SPEED #0.8
            

            elif maptype=="challenge" and value > 2200:
                BP.set_motor_power(rightmotor, -20) 
                BP.set_motor_power(leftmotor, 20) 
                time.sleep(0.1)
                BP.set_motor_power(rightmotor, R_SPEED) 
                BP.set_motor_power(leftmotor, L_SPEED) 
                time.sleep(0.1)
                BP.set_motor_power(rightmotor, 0) 
                BP.set_motor_power(leftmotor, 0)''' 


            BP.set_motor_power(rightmotor, rpower) 
            BP.set_motor_power(leftmotor, lpower) 

            t = time.time() - start_time
            interval = t - old_t
            #odometry calculations go here, get_odometry_dist would find the euclidean distance we’ve travelled so far in this current loop iteration
            end_left = BP.get_motor_encoder(leftmotor) #degrees
            end_right = BP.get_motor_encoder(rightmotor) #degrees
            
            
            vtan_left = ((end_left-start_left)/interval)*(math.pi/180)*RADIUS #inches/second
            vtan_right = ((end_right-start_right)/interval)*(math.pi/180)*RADIUS
            vtan = (vtan_left+vtan_right)/2

            dist = vtan*interval
            curr_dist+=dist
            total_dist+=dist

            hasError = True
            while hasError:
                try:
                    value2=BP.get_sensor(ultrasonic)
                    hasError = False
                except:
                    hasError = True
            samples+=[value2] 

            if not seenBlock and value2>=lower_bound and value2<=upper_bound and curr_dist>0:
                BP.set_motor_power(rightmotor, 0)
                BP.set_motor_power(leftmotor, 0)
                seenBlock=True

                curr_dist=0
                samples=[]
                time.sleep(0.1)
                BP.set_motor_power(rightmotor, rpower)
                BP.set_motor_power(leftmotor, lpower)
            
            if curr_dist>=sect_dist*multiplier and seenBlock:
                BP.set_motor_power(rightmotor, 0)
                BP.set_motor_power(leftmotor, 0)

                avg_sensor_dist=np.median(samples)
                if avg_sensor_dist>=lower_bound and avg_sensor_dist<=upper_bound:
                    obs+=[1]
                else:
                    obs+=[0]
                
                guess, prob, currInfo = map.getLoc(p_map, obs, currInfo)
                print("current position: ", guess, ", with probability: ", prob, "and thinks map has", obs[-1])
                print("sensor avg value: ", avg_sensor_dist)

                samples=[]
                curr_dist=0
                time.sleep(0.1)
                BP.set_motor_power(rightmotor, rpower)
                BP.set_motor_power(leftmotor, lpower)
                if len(obs)>=16 and prob>0.95 and guess==goal:
                    BP.set_motor_power(rightmotor, 0)
                    BP.set_motor_power(leftmotor, 0)
                    BP.reset_all()
                    print(obs, total_dist)
                    break
            old_t=t
            start_left = end_left
            start_right = end_right

        except KeyboardInterrupt:
            BP.set_motor_power(leftmotor, 0)
            BP.set_motor_power(rightmotor, 0)
            BP.reset_all()
            break
    BP.reset_all()


c_map=[0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1] #TA given map of obstacles
goal_state=0
    
localization("challenge", c_map, goal_state)