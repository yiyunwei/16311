from __future__ import division
import time, brickpi3, math

BP = brickpi3.BrickPi3()
PI = math.pi

leftmotor = BP.PORT_A
rightmotor = BP.PORT_D

def RungeKutta(v, theta, x, y, w, time):
    xf = x
    yf = y
    thetaf = theta
    t = time
    k00 = v*math.cos(theta)
    k01 = v*math.sin(theta)
    k2 = w
    
    k10 = v*math.cos(theta+(t/2)*k2)
    k11 = v*math.sin(theta+(t/2)*k2)
        
    x += (t/6)*(k00+5*k10)
    y += (t/6)*(k01+5*k11)
    theta += t*k2
    
    thetaf = theta
    xf = x
    yf = y
    
    return (xf, yf, thetaf)


#target is an x, y, angle tuple
#theta is always 0
def getPosition(radius, wheelbase, target):
    # measurements except angles are all in inches
    pwr = 25
    theta, xi, yi, xf, yf = target
    #assumption. this should always be true of inputs anyways
    theta = 0

    kp = -6
    kd = 1
    ki = 1
    error, power, integral = 0, 0, 0

    prev_t = 0
    start_time = time.time()

    start_left = BP.get_motor_encoder(BP.PORT_A) #degrees
    start_right = BP.get_motor_encoder(BP.PORT_D) #degrees

    BP.set_motor_power(leftmotor, pwr)
    BP.set_motor_power(rightmotor, pwr)

    print(xf,xi)
    while abs(xf-xi) > 0.125 and abs(yf-yi)>0.125:
        print(xf,xi)
        time.sleep(0.01)

        t = time.time() - start_time
        interval = t - prev_t

        try:
            
            end_left = BP.get_motor_encoder(leftmotor) #degrees
            end_right = BP.get_motor_encoder(rightmotor) #degrees

            vtan_left = ((end_left-start_left)/t)*(PI/180)*radius #inches/second
            vtan_right = ((end_right-start_right)/t)*(PI/180)*radius
            vtan = (vtan_left+vtan_right)/2
            vang = (vtan_right-vtan_left)/wheelbase
        
        
            (xi, yi, theta) = RungeKutta(vtan, theta*math.pi/180, xi, yi, vang/radius, t)
            theta = theta*180/math.pi
            print(xi,yi,theta*180/math.pi)


            oldError = error
            error = theta

            diff = error - oldError #for kd term
            integral += (interval)*error #for ki term
            
            power = kp*error + kd*diff + ki*integral
        
            BP.set_motor_power(leftmotor, pwr + power)
            BP.set_motor_power(rightmotor, pwr)
            

            start_left = end_left
            start_right = end_right
            prev_t = t
        
            BP.set_motor_power(leftmotor, 0)
            BP.set_motor_power(rightmotor, 0)

        except KeyboardInterrupt:
            BP.set_motor_power(leftmotor, 0)
            BP.set_motor_power(rightmotor, 0)
            print(xi, target)

    BP.set_motor_power(leftmotor,0)
    BP.set_motor_power(rightmotor,0)

    return (xi,yi,theta)

radius = 1.65625/2
wheelbase = 4
target =  (0,0,0,5,0)
getPosition(radius, wheelbase, target)