from __future__ import division
import time, brickpi3, math

BP = brickpi3.BrickPi3()
PI = math.pi

leftmotor = BP.PORT_A
rightmotor = BP.PORT_D

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
    
    thetaf = theta
    xf = x
    yf = y
    
    return (xf, yf, thetaf)

def turn(angle):

    if angle==-45 or angle==315:
        BP.set_motor_power(leftmotor, 20)
        BP.set_motor_power(rightmotor, -20)
        init_pos_l = (BP.get_motor_encoder(leftmotor))%360
        
        while (BP.get_motor_encoder(leftmotor)-init_pos_l)%360 < 71:
            t = time.time()
    
    elif angle==45 or angle==-315:
        BP.set_motor_power(leftmotor, -20)
        BP.set_motor_power(rightmotor, 20)
        init_pos_r = (BP.get_motor_encoder(rightmotor))%360
        while (BP.get_motor_encoder(rightmotor)-init_pos_r)%360 < 85:
            t = time.time() 

    elif angle==90 or angle==-270:
        BP.set_motor_power(leftmotor, -20)
        BP.set_motor_power(rightmotor, 20)
        init_pos_r = (BP.get_motor_encoder(rightmotor))%360
        while (BP.get_motor_encoder(rightmotor)-init_pos_r)%360 < 167:
            t = time.time() 

    elif angle==-90 or angle==270:
        BP.set_motor_power(leftmotor, 20)
        BP.set_motor_power(rightmotor, -20)
        init_pos_l = (BP.get_motor_encoder(leftmotor))%360
        
        while (BP.get_motor_encoder(leftmotor)-init_pos_l)%360 < 135:
            t = time.time()

    elif angle==135 or angle==-225:
        BP.set_motor_power(leftmotor, -20)
        BP.set_motor_power(rightmotor, 20)
        init_pos_r = (BP.get_motor_encoder(rightmotor))%360
        while (BP.get_motor_encoder(rightmotor)-init_pos_r)%360 < 262:
            t = time.time() 

    elif angle==-135 or angle==225:
        BP.set_motor_power(leftmotor, 20)
        BP.set_motor_power(rightmotor, -20)
        init_pos_l = (BP.get_motor_encoder(leftmotor))%360
        
        while (BP.get_motor_encoder(leftmotor)-init_pos_l)%360 < 210:
            t = time.time()

    #print("left: ",BP.get_motor_status(leftmotor))
    #print("right: ",BP.get_motor_status(rightmotor))

    BP.set_motor_power(leftmotor,0)
    BP.set_motor_power(rightmotor,0)
    time.sleep(0.5)
    return None

#target is an x, y, angle tuple
#theta is always 0
def getPosition(radius, wheelbase, target):
    # measurements except angles are all in inches
    print(BP.get_voltage_battery(),"V\n")
    pwr = 55
    theta, xi, yi, xf, yf = target
    x=0
    y=0

    #dist = max(abs(xi - xf), abs(yi - yf))
    dist = math.sqrt((xf-xi)**2+(yf-yi)**2)

    if dist < 2:
        pwr = 25
    #assumption. this should always be true of inputs anyways
    #theta = 0


    kp = -2
    kd = 0.8
    ki = 0.0001
    error, power, integral = 0, 0, 0

    prev_t = 0
    start_time = time.time()

    start_left = BP.get_motor_encoder(BP.PORT_A) #degrees
    start_right = BP.get_motor_encoder(BP.PORT_D) #degrees

    l = start_left
    r = start_right

    BP.set_motor_power(leftmotor, pwr)
    BP.set_motor_power(rightmotor, pwr)
    #max(abs(x), abs(y))

    while math.sqrt(x**2+y**2)-dist*1.052<0:
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
        
        
            (x, y, theta) = RungeKutta(vtan, theta*math.pi/180, x, y, vang/radius, t)
            theta = theta*180/math.pi
            #print(xi,yi,theta*180/math.pi)

            lefterror = end_left - l
            righterror = end_right - r

            oldError = error
            error = righterror-lefterror

            diff = error - oldError #for kd term
            integral += (interval)*error #for ki term
            
            power = kp*error + kd*diff + ki*integral
            #print(theta, pwr, pwr+power)
        
            BP.set_motor_power(leftmotor, pwr)
            BP.set_motor_power(rightmotor, pwr + power)
            

            start_left = end_left
            start_right = end_right
            prev_t = t
        
            #BP.set_motor_power(leftmotor, 0)
            #BP.set_motor_power(rightmotor, 0)

        except KeyboardInterrupt:
            BP.set_motor_power(leftmotor, 0)
            BP.set_motor_power(rightmotor, 0)
            print(xi, target)
            break


    BP.set_motor_power(leftmotor,0)
    BP.set_motor_power(rightmotor,0)
    time.sleep(0.5)
    print(math.sqrt(x**2+y**2))

    return (x,y,theta)

DIAMETER = 2.24409449 #large grippy tires
RADIUS = DIAMETER/2
WHEELBASE = 3.75


# turn(-135)


#getPosition(RADIUS, WHEELBASE,(0, 5, 5, 65, 5))

#turn(-45)
# time.sleep(1)