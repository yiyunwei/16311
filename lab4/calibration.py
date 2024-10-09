from __future__ import division
from __future__ import print_function
import time, brickpi3, numpy

BP = brickpi3.BrickPi3()

forwardsensor = BP.PORT_3
backwardsensor = BP.PORT_2

BP.set_sensor_type(forwardsensor, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(backwardsensor, BP.SENSOR_TYPE.NXT_LIGHT_ON)

calibrationtime = 5
cycle = 0.2

try:
    timepassed = 0
    forwardtotal = 0
    backwardtotal = 0
    difftotal = []
    while timepassed < calibrationtime:
        time.sleep(cycle) #clock cycle
        timepassed += cycle

        forward = BP.get_sensor(forwardsensor)
        backward = BP.get_sensor(backwardsensor)

        
        difftotal = difftotal + [abs(forward-backward)]

    standarddev = numpy.std(difftotal)
    avg = numpy.average(difftotal)
    
    print("std: ", standarddev, "avg: ", avg)


except KeyboardInterrupt:
    BP.reset_all()