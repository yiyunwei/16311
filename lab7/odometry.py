import math
import brickpi3
import time

BP = brickpi3.BrickPi3()

DIAMETER = 2.24409449 #large grippy tires
RADIUS = DIAMETER/2
WHEELBASE = 0 #TODO: update
SPEED = 50

leftmotor = BP.PORT_D
rightmotor = BP.PORT_A

def RungeKutta(v, theta, x, y, w, t):
    xf = x
    yf = y
    thetaf = theta
    k00 = v*math.cos(theta)
    k01 = v*math.sin(theta)
    
    k10 = v*math.cos(theta+(t/2)*w)
    k11 = v*math.sin(theta+(t/2)*w)
    
    x += (t/6)*(k00+5*k10)
    y += (t/6)*(k01+5*k11)
    theta += t*w
    
    thetaf = theta
    xf = x
    yf = y
    
    return (xf, yf, thetaf)

def getPosition(speed, radius, wheelbase, dist):

    x=0
    y=0
    theta=0

    prev_t = 0
    start_time = time.time()

    start_left = BP.get_motor_encoder(BP.PORT_A) #degrees
    start_right = BP.get_motor_encoder(BP.PORT_D) #degrees

    BP.set_motor_power(leftmotor, speed)
    BP.set_motor_power(rightmotor, speed)
    #max(abs(x), abs(y))

    while math.sqrt(x**2+y**2)<dist:
        time.sleep(0.01)

        t = time.time() - start_time
        interval = t - prev_t

        try:
            
            end_left = BP.get_motor_encoder(leftmotor) #degrees
            end_right = BP.get_motor_encoder(rightmotor) #degrees

            vtan_left = ((end_left-start_left)/t)*(math.pi/180)*radius #inches/second
            vtan_right = ((end_right-start_right)/t)*(math.pi/180)*radius
            vtan = (vtan_left+vtan_right)/2
            vang = (vtan_right-vtan_left)/wheelbase
        
        
            (x, y, theta) = RungeKutta(vtan, theta*math.pi/180, x, y, vang/radius, t)
            theta = theta*180/math.pi

            start_left = end_left
            start_right = end_right
            prev_t = t

        except KeyboardInterrupt:
            BP.set_motor_power(leftmotor, 0)
            BP.set_motor_power(rightmotor, 0)
            break


    BP.set_motor_power(leftmotor,0)
    BP.set_motor_power(rightmotor,0)
    time.sleep(0.5)
    # print(math.sqrt(x**2+y**2))

    return (x,y,theta)

print(getPosition(25,RADIUS, WHEELBASE, (0,0,0,10,0)))