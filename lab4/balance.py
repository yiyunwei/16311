from __future__ import division
from __future__ import print_function
import time, brickpi3, numpy


BP = brickpi3.BrickPi3()
print(BP.get_voltage_battery(),"V\n")

leftmotor = BP.PORT_A
rightmotor = BP.PORT_D

forwardsensor = BP.PORT_3
backwardsensor = BP.PORT_2

times = []
errors = []
powers = []

# constants to be tuned 
kp = -0.55
kd = -0.12
ki= 0#0.1 
             

error = 0                                               
power = 0
integral = 0

BP.set_sensor_type(forwardsensor, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(backwardsensor, BP.SENSOR_TYPE.NXT_LIGHT_ON)

try:

    calibrationtime = 5
    cycle = 0.2

    timepassed = 0
    forwardtotal = 0
    backwardtotal = 0
    difftotal = []
    while timepassed < calibrationtime:
        time.sleep(cycle) #clock cycle
        timepassed += cycle

        forward = BP.get_sensor(forwardsensor)
        backward = BP.get_sensor(backwardsensor)

        
        difftotal = difftotal + [forward-backward]

    # this is the average difference between the sensor readings
    avgdiff = numpy.average(difftotal)
  

    start_time = 0
    old_time = time.time()
    while True:
    
        start_time = time.time()
        
        time.sleep(0.01) #clock cycle
        try:
            # read the light sensor values
            forward = BP.get_sensor(forwardsensor)
            backward = BP.get_sensor(backwardsensor)
            
            oldError = error
            error = (forward - backward) - avgdiff

            diff = error - oldError #for kd term
            integral += (old_time-start_time)*error #for ki term
            
            oldPower = power
            power = kp*error + kd*diff + ki*integral
            
            if (oldPower < 0 and power > 0) or (oldPower > 0 and power < 0):
                integral = (old_time-start_time)*error
         
            BP.set_motor_power(leftmotor, power)
            BP.set_motor_power(rightmotor, power)
            
            old_time = start_time

        except:
            BP.set_motor_power(leftmotor,0)
            BP.set_motor_power(rightmotor,0)
            BP.reset_all()

except KeyboardInterrupt:
    BP.set_motor_power(leftmotor,0)
    BP.set_motor_power(rightmotor,0)
    BP.reset_all()
    