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
ultrasonic = BP.PORT_1

BP.set_sensor_type(ultrasonic, BP.SENSOR_TYPE.NXT_ULTRASONIC)

time.sleep(3) #need delay after initializing so that sensor readings don't break

BP.set_motor_power(rightmotor, 0)
BP.set_motor_power(leftmotor, 0)


def RungeKutta(v, theta, x, y, w, t):
    xf = x
    yf = y
    thetaf = theta
    k00 = v*math.cos(theta)
    k01 = v*math.sin(theta)
    
    k10 = v*math.cos(theta+(t/2)*w)
    k11 = v*math.sin(theta+(t/2)*w)
    
    #our issue probably has to do with these
    x += (t/6)*(k00+5*k10)
    y += (t/6)*(k01+5*k11)
    theta += t*w
    
    thetaf = theta % math.pi*2
    xf = x
    yf = y
    
    return (xf, yf, thetaf)




def followLine(SPEED, maptype):
    seenblack = True
    direction = RIGHT #turning right initially
    adj = False
    x,y,theta = 0,0,0
    dist = 0
    while True:
        try:
            try:

                start_time = time.time()

                start_left = BP.get_motor_encoder(BP.PORT_A) #degrees
                start_right = BP.get_motor_encoder(BP.PORT_D) #degrees

                BP.set_motor_power(leftmotor, SPEED)
                BP.set_motor_power(rightmotor, SPEED)


                value = BP.get_sensor(lightport)  
                lpower = SPEED

                if (value < 1800 and seenblack): #sensing white, coming off of black
                    if direction==LEFT:
                        direction = RIGHT
                        rpower = 0.5*SPEED
                        # print("turning right", value)
                    elif direction== RIGHT:
                        direction = LEFT
                        rpower = SPEED #*0.95
                        # print("turning left", value)
                    seenblack = False
                elif value < 1800: #sensing white having been on white
                    if direction==LEFT:
                        rpower = (SPEED)
                        # print("keep left")
                    elif direction== RIGHT:
                        rpower = -0.5*(SPEED)
                        # print("keep right")
                elif value > 2100:                                                                                             
                    if(direction == LEFT):
                        direction = RIGHT
                        rpower = -0.75*(SPEED)
                        # print("overadjusting")
                        adj = True
                    else:
                        direction = RIGHT
                        if maptype=="regular":
                            rpower = 0.55*SPEED #0.67
                        else:
                            rpower = 0.6*SPEED
                        # print("yahoo")
                    seenblack = True     
                else:                    
                    if maptype=="regular":
                        rpower = SPEED*0.57
                    else:
                        rpower = (SPEED)*.57
                    # print("yippee")
                BP.set_motor_power(rightmotor, rpower) 
                BP.set_motor_power(leftmotor, lpower)

                if adj == True: 
                    time.sleep(0.5)
                else:
                    time.sleep(0.03) 
                adj = False        


                DIAMETER = 2.24409449 #large grippy tires
                RADIUS = DIAMETER/2
                WHEELBASE = 7.25  

                t = time.time() - start_time

        
                end_left = BP.get_motor_encoder(leftmotor) #degrees
                end_right = BP.get_motor_encoder(rightmotor) #degrees

                vtan_left = ((end_left-start_left)/t)*(math.pi/180)*RADIUS #inches/second
                vtan_right = ((end_right-start_right)/t)*(math.pi/180)*RADIUS
                vtan = (vtan_left+vtan_right)/2
                
                vang = (vtan_right-vtan_left)/WHEELBASE


                (x, y, theta) = RungeKutta(vtan, theta, x, y, vang/RADIUS, t) # theta*math.pi/180
                dist+=math.sqrt(x**2+y**2)
                print("distance: ",dist)
   
               
            except brickpi3.SensorError as error:
                print(error)
                BP.set_motor_power(leftmotor,0)
                BP.set_motor_power(rightmotor,0)
                BP.reset_all()
                break

        except KeyboardInterrupt:
            BP.set_motor_power(leftmotor,0)
            BP.set_motor_power(rightmotor,0)
            BP.reset_all()

def getPosition(speed, radius, wheelbase, x,y,theta):

    # start_time = time.time()

    # start_left = BP.get_motor_encoder(BP.PORT_A) #degrees
    # start_right = BP.get_motor_encoder(BP.PORT_D) #degrees

    # BP.set_motor_power(leftmotor, speed)
    # BP.set_motor_power(rightmotor, speed)

    # t = time.time() - start_time

        
    end_left = BP.get_motor_encoder(leftmotor) #degrees
    end_right = BP.get_motor_encoder(rightmotor) #degrees

    vtan_left = ((end_left-start_left)/t)*(math.pi/180)*radius #inches/second
    vtan_right = ((end_right-start_right)/t)*(math.pi/180)*radius
    vtan = (vtan_left+vtan_right)/2
    return vtan*t
    # vang = (vtan_right-vtan_left)/wheelbase


    # (x, y, theta) = RungeKutta(vtan, theta, x, y, vang/radius, t) # theta*math.pi/180
   
    # theta = theta*180/math.pi
    # #print(xi,yi,theta*180/math.pi)

    # lefterror = end_left - l
    # righterror = end_right - r

    # oldError = error
    # error = righterror-lefterror

    # diff = error - oldError #for kd term
    # integral += (interval)*error #for ki term
    
    # power = kp*error + kd*diff + ki*integral
    # #print(theta, pwr, pwr+power)

    # BP.set_motor_power(leftmotor, speed)
    # BP.set_motor_power(rightmotor, speed + power)
    

    # start_left = end_left
    # start_right = end_right
    # prev_t = t


    # BP.set_motor_power(leftmotor,0)
    # BP.set_motor_power(rightmotor,0)
    # # time.sleep(0.5)

    return (x,y,theta)

followLine(25, "regular")