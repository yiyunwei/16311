import cv2 
import numpy as np 
import math
import brickpi3
import time

from lab7.odometry import getPosition

#replace with whatever our image is called
  
image1 = cv2.imread('./test.jpg') 

image1 = cv2.imread('./arrow_demo.png') 

# convert image to grey
img = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV) 

print("shape", img.shape)

height, width, _ = img.shape

thresh = cv2.inRange(img, (104, 117, 65), (136, 255, 96))

red_thresh = cv2.inRange(img, (175, 123, 119), (180, 255, 247))

col_sum=0
col_count=0
max_count=0
biggest_col=-1


for c in range(width):
    curr_count=0
    for r in range(height):
        if thresh[r, c]==255:
            curr_count+=1
            col_sum+=c
            col_count+=1
            if curr_count>max_count:
                max_count=curr_count
                biggest_col=c

avg_col=col_sum/col_count
arrow_dir_sign=biggest_col-avg_col
arrow_dir="left"
if arrow_dir_sign>0:
    arrow_dir="right"

print(arrow_dir_sign, arrow_dir)


centroid_x=0
centroid_y=0
wrong_centroid_x=0
wrong_centroid_y=0
wrong_count=0
count=0

for c in range(width):
    for r in range(height):
        if red_thresh[r, c]==255 and ((c>biggest_col and arrow_dir=="right") or (c<biggest_col and arrow_dir=="left")):
            count+=1
            centroid_x+=c
            centroid_y+=r
        elif red_thresh[r, c]==255 and ((c<biggest_col and arrow_dir=="right") or (c>biggest_col and arrow_dir=="left")):
            wrong_count+=1
            wrong_centroid_x+=c
            wrong_centroid_y+=r



centroid_x=centroid_x/count
centroid_y=centroid_y/count

print("ball location we want is x: ", centroid_x, " y: ", centroid_y)

wrong_centroid_x=wrong_centroid_x/wrong_count
wrong_centroid_y=wrong_centroid_y/wrong_count

print("ball location we don't want is x: ", wrong_centroid_x, " y: ", wrong_centroid_y)

pixel_dist = math.sqrt((centroid_x-wrong_centroid_x)**2+(centroid_y-wrong_centroid_y)**2)
print("pixel_dist", pixel_dist)
focal_length_pixels = 4.74*math.sqrt(11943936)/7.4
print("focal_length_pixels: ", focal_length_pixels)

dist_ratio = pixel_dist/5
print("dist_ratio: ", dist_ratio)
dist_in = focal_length_pixels / dist_ratio



#need to go dist_in forward, 2.5 in arrow direction w arm raised
BP = brickpi3.BrickPi3()
armmotor = BP.PORT_C
leftmotor = BP.PORT_D
rightmotor = BP.PORT_A
BP.set_motor_power(armmotor, 100)
time.sleep(2)
BP.set_motor_power(armmotor, 0)
rad_in = 2.125
wheelbase_in = 7
getPosition(40, rad_in, wheelbase_in, dist_in)

if arrow_dir == "right":
    BP.set_motor_dps(leftmotor, 50)
    BP.set_motor_dps(rightmotor, -50)

    start_Time = time.time()
    time.sleep(0.01)
    end_Time = time.time()
    while end_Time - start_Time < 2:
        end_Time = time.time()
else:
    BP.set_motor_dps(leftmotor, -50)
    BP.set_motor_dps(rightmotor, 50)

    start_Time = time.time()
    time.sleep(0.01)
    end_Time = time.time()
    while end_Time - start_Time < 2:
        end_Time = time.time()
BP.set_motor_dps(leftmotor, 0)
BP.set_motor_dps(rightmotor, 0)

getPosition(40, rad_in, wheelbase_in, 2.5)




print("go forward: ", dist_in, " and ", arrow_dir, " 2.5 in")
