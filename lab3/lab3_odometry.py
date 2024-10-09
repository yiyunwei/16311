from __future__ import division
import time, brickpi3, math

BP = brickpi3.BrickPi3()

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

def initOdometry(pair1, pair2, pair3):
    x,y,theta = 0,0,0
    prev_t=0 #dividing 3 by t must produce an integer
    #interval = int(3/t)
    try:
        for (left, right) in [pair1, pair2, pair3, (0,0)]:
            start_time = time.time()
            
            start_left = BP.get_motor_encoder(BP.PORT_A) #degrees
            start_right = BP.get_motor_encoder(BP.PORT_D) #degrees
            #start_left = 0
            #start_right = 0
            #print(start_left)
    
#                
            BP.set_motor_power(BP.PORT_A, left) #PWM signals
            BP.set_motor_power(BP.PORT_D, right)
            t = time.time() - start_time
            while t < 3:
                t = time.time() - start_time
                interval = t - prev_t
                try:
                
                    #measurements are all in inches
                
                    
                
                    #time.sleep(t)
                    end_left = BP.get_motor_encoder(BP.PORT_A) #degrees
                    end_right = BP.get_motor_encoder(BP.PORT_D) #degrees
                    
                    
                    #print(end_left)

                    vtan_left = (end_left-start_left)/t*3.14159/180*1.125 #inches/second
                    vtan_right = (end_right-start_right)/t*3.14159/180*1.125
                    vtan = (vtan_left+vtan_right)/2
                    vang = (vtan_right-vtan_left)/6.375
                    #print(vtan)
                
                
                    (x, y, theta) = RungeKutta(vtan, theta, x, y, vang/1.125, t)
                    
                    start_left = end_left
                    start_right = end_right
                    prev_t = t
                    
                
                except IOError as error:
                    print(error)
            BP.set_motor_power(BP.PORT_A, 0)
            BP.set_motor_power(BP.PORT_D,0)
            print(vang, x, y, theta*180/3.14159)
    except KeyboardInterrupt:
        BP.set_motor_power(BP.PORT_A, 0)
        BP.set_motor_power(BP.PORT_D,0)
    
    return (x,y)

initOdometry((-26,-23),(12,-17),(-25,20))