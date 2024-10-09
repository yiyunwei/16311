from __future__ import print_function 
from __future__ import division
import brickpi3, time
from map import construct_map

BP = brickpi3.BrickPi3()
print(BP.get_voltage_battery())

limb1 = BP.PORT_D
limb2 = BP.PORT_A

BP.set_motor_position(limb1, 0)
BP.set_motor_position(limb2, 0) #-20 = at the zero line
time.sleep(5)

def runangles(angleinput):
    #BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    # BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    #print(BP.get_motor_encoder(limb1), BP.get_motor_encoder(limb2))

    #angles = [] #getangles
    angles = angleinput
    newangles = []

    if len(angles)!=0:
        newangles += tuple([angles[0]])
        temp = angles[0]
    changed = None

    direction = 1
    # for i in range(len(angles)):
    #     curr = angles[i]
    #     if (i > 0):
    #         prev = angles[i-1]
    #         if(curr[1] > prev[1]):
    #             if(direction != 1):
    #                 angles[i] = (curr[0], curr[1] + 10)
    #             direction = 1
    #         elif(curr[1] < prev[1]):
    #             if(direction != -1):
    #                 angles[i] = (curr[0], curr[1] - 10)
    #             direction = -1

    for i in range(len(angles)):
        pair = angles[i]

        #overshooting when changing directions
        # if (pair[0] != temp[0]) and (pair[1] != temp[1]):
        #     prev = angles[i-1]
        #     if(pair[1] > prev[1]):
        #         pair = tuple([pair[0], pair[1] + 10])
        #     elif(pair[1] < prev[1]):
        #         pair = tuple([pair[0] + 10, pair[1]])

        #     newangles += tuple([prev])
        #     temp = prev

        #so the robot doesnt go the wrong way from 350 to 0 or vice versa
        if (i != 0):
            prev = angles[i-1]
            # if(prev[0] == 350 and pair[0] == 0):
            #     pair = tuple([360, pair[1]])
            #     angles[i] = pair
            # elif(prev[1] == 350 and pair[1] == 0):
            #     pair = tuple([pair[0], 360])
            #     angles[i] = pair
            # elif(prev[0] == 0 and pair[0] == 350):
            #     pair = tuple([-10, pair[1]])
            #     angles[i] = pair
            # elif(prev[1] == 0 and pair[1] == 350):
            #     pair = tuple([pair[0], -10])
            #     angles[i] = pair

            # if(prev[0] >= 360):
            #     pair = tuple([pair[0] + 360, pair[1]])
            #     angles[i] = pair
            # elif(prev[1] >= 360):
            #     pair = tuple([pair[0], pair[1] + 360])
            #     angles[i] = pair
            # elif(prev[0] < 0 and pair[0] != 0):
            #     pair = tuple([pair[0] - 360, pair[1]])
            #     angles[i] = pair
            # elif(prev[1] < 0 and pair[1] != 0):
            #     pair = tuple([pair[0], pair[1] - 360])
            #     angles[i] = pair

        # if(pair[0] != temp[0]):
        #     prev = angles[i-1]
        #     if(changed != 0):
        #         newangles += tuple([pair])
        #         temp = pair
        #     changed = 0
        # elif(pair[1] != temp[1]):
        #     prev = angles[i-1]
        #     if(changed != 1):
        #         newangles += tuple([pair])
        #         temp = pair
        #     changed = 1

    if len(angles)!=0:
        newangles += [angles[-1]]

    #print(newangles)

    print(angles)

    for angle in angles:
        BP.set_motor_position(limb1, angle[0]-10) #-10
        BP.set_motor_position(limb2, angle[1]) #-20
        time.sleep(0.3)
    time.sleep(8)

tuple1, soln1 = construct_map(6.25, 0, 0, 0, 3, 2)
pos_x1, pos_y1, t1, t2 = tuple1
tuple2, soln2 = construct_map(pos_x1, pos_y1, t1, t2, 0, 4)
pos_x2, pos_y2, t1, t2 = tuple2
_, soln3 = construct_map(pos_x2, pos_y2, t1, t2, -3, 2)

runangles(soln1)

runangles(soln2)

runangles(soln3)

#runangles([(110, 10), (110, 0), (100, 0), (100, 350)])