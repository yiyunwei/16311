"""
File:           construct_map.py
Date:           3/2/2021
Description:    lab5 code for contructing a map from obstacle coordinates 
Author:         Abha Agrawal (abhaa@andrew.cmu.edu)

"""

import math
from operator import truediv
import random
import numpy
import matplotlib.pyplot as plt
from queue import PriorityQueue
import time


MAP_WIDTH=72
MAP_HEIGHT=54

frac_size = 8

def calculate_intersect(l1, l2):

        x_lowerb=max(l1.x1, l2.x1)
        x_upperb=min(l1.x2, l2.x2)

        soln_x=None
        soln_y=None

        if l1.m!=None and l2.m!=None:
            intersect_x=(l2.b-l1.b)/(l1.m-l2.m)
            intersect_y=l1.m*intersect_x+l1.b
            if intersect_x>=x_lowerb and intersect_x<=x_upperb:
                soln_x=intersect_x
                soln_y=intersect_y
        elif l1.m!=None:
            if l2.x1>=x_lowerb and l2.x2<=x_upperb:
                soln_x=l2.x1
                soln_y=l1.m*soln_x+l1.b
        elif l2.m!=None:
            if l1.x1>=x_lowerb and l1.x2<=x_upperb:
                soln_x=l1.x1
                soln_y=l2.m*soln_x+l2.b
        
        return (soln_x, soln_y)


class Line:
    # line defined by p1, p2
    #so in our implementation this is a line segment

    def __init__(self, p1, p2):
        # @TODO fill this in 
        (self.x1, self.y1)=p1
        (self.x2, self.y2)=p2

        #order points -- relevant for later
        if self.x2<self.x1:
            (self.x1, self.y1)=p2
            (self.x2, self.y2)=p1

        #bug catching for x=a line case    
        self.m=None
        self.b=None
        if self.x1-self.x2!=0:
            self.m=(self.y2-self.y1)/(self.x2-self.x1)
            self.b=self.y1-self.m*self.x1

    def onLine(self, p1):
        x, y = p1
        if self.m!=None:
            if self.m*x+self.b==y:
                return True
            return False
        return (x==self.x1)

class Obstacle:
    
    # the arguments are all objects of Line
    # ls are the lower bounders
    # us are the upper bounders
    #make the new padded object
    def __init__(self, l1, l2, u1, u2):
        # @TODO fill this in 

        #padding is in inches, if we change the size of 
        #grid square we will also have to change this
        padding=5.125
        lines=[l1, l2, u1, u2]
        min_y=min(u1.y1, u1.y2, u2.y1, u2.y2, l1.y1, l1.y2, l2.y1, l2.y2)
        min_x=min(u1.x1, u1.x2, u2.x1, u2.x2, l1.x1, l1.x2, l2.x1, l2.x2)
        max_y=max(u1.y1, u1.y2, u2.y1, u2.y2, l1.y1, l1.y2, l2.y1, l2.y2)
        max_x=max(u1.x1, u1.x2, u2.x1, u2.x2, l1.x1, l1.x2, l2.x1, l2.x2)

        for i in range(4):
            if lines[i].x1==min_x:
                lines[i].x1-=padding
            if lines[i].x1==max_x:
                lines[i].x1+=padding
            if lines[i].y1==min_y:
                lines[i].y1-=padding
            if lines[i].y1==max_y:
                lines[i].y1+=padding

            if lines[i].x2==min_x:
                lines[i].x2-=padding
            if lines[i].x2==max_x:
                lines[i].x2+=padding
            if lines[i].y2==min_y:
                lines[i].y2-=padding
            if lines[i].y2==max_y:
                lines[i].y2+=padding

            if lines[i].m != None:
                lines[i].b=lines[i].y1-lines[i].m*lines[i].x1

        self.l1=lines[0]
        self.l2=lines[1]
        self.u1=lines[2]
        self.u2=lines[3]

                    

    
        
    
    # returns true if x,y is in the obstacle, false otherwise
    def clash(self, x, y):
        # @TODO fill this in 

        #assuming in square case that the u1/2 of the 
        #form x=a is more + than the l1/2 with x=a

        if x<5 or x>67 or y<5 or y>49:
            return True

        past_l1 = self.l1.x1<=x 
        past_l2 = self.l2.x1<=x
        before_u1 = self.u1.x2>=x
        before_u2 = self.u2.x2>=x

        
        if self.l1.m!=None:
            past_l1 = (self.l1.m*x+self.l1.b<=y)
        if self.l2.m!=None:
            past_l2 = (self.l2.m*x+self.l2.b<=y)
        if self.u1.m!=None:
            before_u1 = (self.u1.m*x+self.u1.b>=y)
        if self.u2.m!=None:
            before_u2 = (self.u2.m*x+self.u2.b>=y)
        

        if past_l1 and past_l2 and before_u1 and before_u2:
            return True
        return False



def construct_obstacles(map):
    # construct obstacles
    # @TODO fill this in 
    obstacles = []

    #easy obstacles
    if map=='easy':
        #Obstacle 1 -- small top square
        Line1 = Line((16, 50), (22, 50))
        Line2 = Line((22, 44), (22, 50))
        Line3 = Line((16, 44), (22, 44))
        Line4 = Line((16, 44), (16, 50))
        Obstacle1 = Obstacle(Line3, Line4, Line1, Line2)

        #Obstacle 2 -- small bottom square
        Line1 = Line((8, 18), (14, 18))
        Line2 = Line((14, 18), (14, 12))
        Line3 = Line((8, 12), (14, 12))
        Line4 = Line((8, 12), (8, 18))
        Obstacle2 = Obstacle(Line3, Line4, Line1, Line2)

        #Obstacle 3 -- vertical rectangle
        Line1 = Line((18, 30), (24, 30))
        Line2 = Line((24, 12), (24, 30))
        Line3 = Line((18, 12), (24, 12))
        Line4 = Line((18, 12), (18, 30))

        Obstacle3 = Obstacle(Line3, Line4, Line1, Line2)

        #Obstacle 4 -- horizontal rectangle
        Line1 = Line((38, 42), (56, 42))
        Line2 = Line((56, 42), (56, 36))
        Line3 = Line((38, 36), (56, 36))
        Line4 = Line((38, 42), (38, 36))

        Obstacle4 = Obstacle(Line3, Line4, Line1, Line2)

    elif map=='hard':
        #follow convention of left, bottom, right, top
        #hard obstacles
        #Obstacle 1 -- big square
        Line1 = Line((23, 19), (23, 28))
        Line2 = Line((23, 19), (33.25, 19))
        Line3 = Line((33.25, 19), (33.25, 28))
        Line4 = Line((23, 28), (33.25, 28))
        Obstacle1 = Obstacle(Line1, Line2, Line3, Line4)

        #Obstacle 2 -- small square
        Line1 = Line((6, 34.5), (6, 40.5))
        Line2 = Line((6, 34.5), (12, 34.5))
        Line3 = Line((12, 34.5), (12, 40.5))
        Line4 = Line((6, 40.5), (12, 40.5))
        Obstacle2 = Obstacle(Line1, Line2, Line3, Line4)

        #Obstacle 3 -- bottom rectangle
        Line1 = Line((39.757, 8.243), (44, 4))
        Line2 = Line((44, 4), (56.728, 16.728))
        Line3 = Line((56.728, 16.728), (52.485, 20.971))
        Line4 = Line((39.757, 8.243), (52.485, 20.971))

        Obstacle3 = Obstacle(Line1, Line2, Line3, Line4)

        #Obstacle 4 -- top rectangle
        Line1 = Line((35.757, 45.757), (48.485, 33.029))
        Line2 = Line((48.485, 33.029), (52.728, 37.272))
        Line3 = Line((40, 50), (52.728, 37.272))
        Line4 = Line((35.757, 45.757), (40, 50))

        Obstacle4 = Obstacle(Line1, Line2, Line3, Line4)
    else:
        print("Invalid map parameter")


    obstacles = [Obstacle1, Obstacle2, Obstacle3, Obstacle4]
    
    return obstacles #array of obstacles

def heuristic(x, y, goal_x, goal_y):
    #theoretically go diagonal for shared distance and then 
    #go either vertical or horizontal depending on what's left over
    return max(abs(goal_x - x), abs(goal_y - y))

class Obstacle_2:
    
    # the arguments are all objects of Line
    # ls are the lower bounders
    # us are the upper bounders
    #make the new padded object
    def __init__(self, l1, l2, u1, u2):
        # @TODO fill this in 

        #padding is in inches, if we change the size of 
        #grid square we will also have to change this
        padding=5.5
        lines=[l1, l2, u1, u2]
        min_y=min(u1.y1, u1.y2, u2.y1, u2.y2, l1.y1, l1.y2, l2.y1, l2.y2)
        min_x=min(u1.x1, u1.x2, u2.x1, u2.x2, l1.x1, l1.x2, l2.x1, l2.x2)
        max_y=max(u1.y1, u1.y2, u2.y1, u2.y2, l1.y1, l1.y2, l2.y1, l2.y2)
        max_x=max(u1.x1, u1.x2, u2.x1, u2.x2, l1.x1, l1.x2, l2.x1, l2.x2)

        for i in range(4):
            if lines[i].x1==min_x:
                lines[i].x1-=padding
            if lines[i].x1==max_x:
                lines[i].x1+=padding
            if lines[i].y1==min_y:
                lines[i].y1-=padding
            if lines[i].y1==max_y:
                lines[i].y1+=padding

            if lines[i].x2==min_x:
                lines[i].x2-=padding
            if lines[i].x2==max_x:
                lines[i].x2+=padding
            if lines[i].y2==min_y:
                lines[i].y2-=padding
            if lines[i].y2==max_y:
                lines[i].y2+=padding

            if lines[i].m != None:
                lines[i].b=lines[i].y1-lines[i].m*lines[i].x1

        self.l1=lines[0]
        self.l2=lines[1]
        self.u1=lines[2]
        self.u2=lines[3]

                    

    
        
    
    # returns true if x,y is in the obstacle, false otherwise
    def clash(self, x, y):
        # @TODO fill this in 

        #assuming in square case that the u1/2 of the 
        #form x=a is more + than the l1/2 with x=a

        if x<5 or x>67 or y<5 or y>49:
            return True

        past_l1 = self.l1.x1<=x 
        past_l2 = self.l2.x1<=x
        before_u1 = self.u1.x2>=x
        before_u2 = self.u2.x2>=x

        
        if self.l1.m!=None:
            past_l1 = (self.l1.m*x+self.l1.b<=y)
        if self.l2.m!=None:
            past_l2 = (self.l2.m*x+self.l2.b<=y)
        if self.u1.m!=None:
            before_u1 = (self.u1.m*x+self.u1.b>=y)
        if self.u2.m!=None:
            before_u2 = (self.u2.m*x+self.u2.b>=y)
        

        if past_l1 and past_l2 and before_u1 and before_u2:
            return True
        return False



def construct_obstacles2(map):
    # construct obstacles
    # @TODO fill this in 
    obstacles = []

    #easy obstacles
    if map=='easy':
        #Obstacle 1 -- small top square
        Line1 = Line((16, 50), (22, 50))
        Line2 = Line((22, 44), (22, 50))
        Line3 = Line((16, 44), (22, 44))
        Line4 = Line((16, 44), (16, 50))

        Obstacle1 = Obstacle_2(Line3, Line4, Line1, Line2)

        #Obstacle 2 -- small bottom square
        Line1 = Line((8, 18), (14, 18))
        Line2 = Line((14, 18), (14, 12))
        Line3 = Line((8, 12), (14, 12))
        Line4 = Line((8, 12), (8, 18))
        Obstacle2 = Obstacle_2(Line3, Line4, Line1, Line2)

        #Obstacle 3 -- vertical rectangle
        Line1 = Line((18, 30), (24, 30))
        Line2 = Line((24, 12), (24, 30))
        Line3 = Line((18, 12), (24, 12))
        Line4 = Line((18, 12), (18, 30))

        Obstacle3 = Obstacle_2(Line3, Line4, Line1, Line2)

        #Obstacle 4 -- horizontal rectangle
        Line1 = Line((38, 42), (56, 42))
        Line2 = Line((56, 42), (56, 36))
        Line3 = Line((38, 36), (56, 36))
        Line4 = Line((38, 42), (38, 36))

        Obstacle4 = Obstacle_2(Line3, Line4, Line1, Line2)


    obstacles = [Obstacle1, Obstacle2, Obstacle3, Obstacle4]
    
    return obstacles #array of obstacles



def construct_map(pos_x, pos_y, goal_x, goal_y, map):

    obstacles = construct_obstacles(map)
    obstacle2s = construct_obstacles2(map)

    # run through all x,y points
    x_cm = MAP_WIDTH  # @TODO need to define MAP_WIDTH at the top 
    y_cm = MAP_HEIGHT # @TODO need to define MAP_HEIGHT at the top 
    
    img = numpy.zeros((x_cm*frac_size+1, y_cm*frac_size+1, 3), dtype=numpy.uint8)

    # @TODO update img matrix based on obstacle coordinates
    '''for row in range(y_cm*frac_size):
        for col in range(x_cm*frac_size):
            for obstacle in obstacles:
                if obstacle.clash(col/frac_size, row/frac_size):
                    img[col][row] = 255'''

    #plt.imshow(img, cmap=plt.cm.gray)
    #plt.show()

    # pos_x = 5
    # pos_y = 5
    pos_dist = 0
    # goal_x = 67
    # goal_y = 49
    paths = PriorityQueue()

    #use convention of adding things to the front of the path
    #heuristic = steps taken + dist to goal
    #last term is total distance
    h=heuristic(pos_x, pos_y, goal_x, goal_y)
    paths.put((h, ([(pos_x, pos_y)], 0)))
    path = []
    visited = [(pos_x, pos_y)]
    init_time=time.time()
    
    #not working rn, keeps printing straight line path
    while not paths.empty():
        path = paths.get()
        posAry, pos_dist = path[1]
        pos_x, pos_y = posAry[0]


        
        if pos_x == goal_x and pos_y == goal_y:
            soln_time = int(time.time()-init_time)
            print("found solution in ", soln_time//60, "minutes and ", soln_time%60, " seconds")
            break

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_x = pos_x+i/frac_size
                new_y = pos_y+j/frac_size
                if (i!=0 or j!=0) and new_x>=0 and new_x<=MAP_WIDTH and new_y>=0 and new_y<=MAP_HEIGHT:
                    newH = heuristic(new_x, new_y, goal_x, goal_y)+(pos_dist+1/frac_size)*0.11
                    canPut = True
                    if abs(new_x-goal_x) > abs(pos_x-goal_x):
                        newH += 1

                    if abs(new_y-goal_y) > abs(pos_y-goal_y):
                        newH += 1
                    if ((new_x, new_y) not in posAry) and ((new_x, new_y) not in visited):
                        for obstacle in obstacles:
                        
                            if obstacle.clash(new_x, new_y):
                                canPut = False
                                break
                        if canPut: 
                            for obstacle in obstacle2s:
                        
                                if obstacle.clash(new_x, new_y):
                                    newH += 1
                            
                            paths.put((newH, ([(new_x, new_y)]+posAry, pos_dist+1/frac_size)))
                            visited += [(new_x, new_y)]
        
    
    for term in posAry:
        x, y = term
        x_coord = x*frac_size
        y_coord = y*frac_size
        #x_coord = x
        #y_coord = y
        img[int(x_coord)][int(y_coord)][0] = 255
    
    
    '''
    #plt.imshow(img.transpose()) #cmap=plt.cm.gray
    img = numpy.rot90(img, 1)
    plt.imshow(img)
    plt.xlabel("x (1/8 inches)")
    plt.ylabel("y (1/8 inches)")
    ax = plt.gca()
    ax.set_xticks(numpy.arange(0, 577, 48))
    ax.set_yticks(numpy.arange(0, 433, 48))
    ax.set_xticklabels(numpy.arange(0, 75, 6))
    ax.set_yticklabels(numpy.arange(54, -1, -6))
    #plt.xticks(numpy.arange(0, 72, 8))
    plt.show()
    '''
    
    return posAry[::-1]




def process_coords(path, init_angle):
    if len(path)==1:
        print("no path found")
        soln = None
    else:
        init_x, init_y = path[0]
        fin_x, fin_y = path[1]
        curr_line = Line((init_x, init_y), (fin_x, fin_y))
        theta = -90
        if init_y < fin_y:
            theta=90
        if curr_line.m!=None:
            theta=math.atan(curr_line.m)*180/math.pi
            if fin_x < init_x:
                print("flip")
                theta+=180
        newPath = path[2:]
        soln=[]
        for coords in newPath:
            if not curr_line.onLine(coords):
                net_angle_turn = theta - init_angle
                soln+=[(net_angle_turn, init_x, init_y, fin_x, fin_y)]
                init_angle = theta
                init_x, init_y = fin_x, fin_y
                fin_x, fin_y = coords
                curr_line = Line((init_x, init_y), (fin_x, fin_y))
                theta = -90
                if init_y < fin_y:
                    theta=90
                if curr_line.m!=None:
                    theta=math.atan(curr_line.m)*180/math.pi
                    if fin_x < init_x:
                        print("flip")
                        theta+=180
            else:
                fin_x, fin_y=coords

        net_angle_turn = theta - init_angle
        soln+=[(net_angle_turn, init_x, init_y, fin_x, fin_y)]

        print("motor commands: ", soln)
    return soln



