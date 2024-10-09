import math
from operator import truediv
import numpy
#import matplotlib.pyplot as plt
from queue import PriorityQueue
import time


MAP_X_MIN=-7
MAP_X_MAX=7
MAP_Y_MIN=0
MAP_Y_MAX=8

frac_size = 8.0

len_1 = 3.875
len_2 = 2.5625

class Line:
    # line defined by p1, p2
    #so in our implementation this is a line segment

    def __init__(self, p1, p2):
        
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

class Obstacle:
    
    # the arguments are all objects of Line
    # ls are the lower bounders
    # us are the upper bounders
    #make the new padded object
    def __init__(self, l1, l2, u1, u2):
        # @TODO fill this in 

        #padding is in inches
        #padding=0.375
        padding = 0.5
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

        if x<MAP_X_MIN or x>MAP_X_MAX or y<MAP_Y_MIN or y>MAP_Y_MAX:
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

def construct_obstacles():
    
    obstacles = []
    #Obstacle 1 -- left square
    Line1 = Line((-4, 4), (-4, 6))
    Line2 = Line((-4, 4), (-2, 4))
    Line3 = Line((-4, 6), (-2, 6))
    Line4 = Line((-2, 4), (-2, 6))
    Obstacle1 = Obstacle(Line1, Line2, Line3, Line4)

    #Obstacle 2 -- vertical part of middle obstacle
    Line1 = Line((-1, 1), (0, 1))
    Line2 = Line((-1, 1), (-1, 3))
    Line3 = Line((-1, 3), (0, 3))
    Line4 = Line((0, 1), (0, 3))
    Obstacle2 = Obstacle(Line1, Line2, Line3, Line4)

    #Obstacle 3 -- horizontal part of middle obstacle
    Line1 = Line((-1, 2), (1, 2))
    Line2 = Line((-1, 2), (-1, 3))
    Line3 = Line((-1, 3), (1, 3))
    Line4 = Line((1, 2), (1, 3))

    Obstacle3 = Obstacle(Line1, Line2, Line3, Line4)

    #Obstacle 4 -- right square
    Line1 = Line((1, 5), (3, 5))
    Line2 = Line((1, 5), (1, 7))
    Line3 = Line((1, 7), (3, 7))
    Line4 = Line((3, 5), (3, 7))

    Obstacle4 = Obstacle(Line1, Line2, Line3, Line4)


    obstacles = [Obstacle1, Obstacle2, Obstacle3, Obstacle4]
    
    return obstacles

def heuristic(x, y, goal_x, goal_y):

    return math.sqrt((abs(goal_x - x))**2 + (abs(goal_y - y))**2)


def construct_map(pos_x, pos_y, theta1, theta2, goal_x, goal_y):

    print(pos_x, pos_y, theta1, theta2, goal_x, goal_y)

    obstacles = construct_obstacles()

    map_width = MAP_X_MAX-MAP_X_MIN  
    map_height = MAP_Y_MAX-MAP_Y_MIN 

    img = numpy.zeros((map_height*int(frac_size)+1, map_width*int(frac_size)+1, 3), dtype=numpy.uint8)
    max_row=int(map_height*frac_size)
    center_col=int((map_width*int(frac_size))/2)

    for row in range(int(map_height*frac_size+1)):
        for col in range(int(map_width*frac_size+1)):
            for obstacle in obstacles:

                if obstacle.clash(col/frac_size+MAP_X_MIN, row/frac_size+MAP_Y_MIN):
                    img[max_row-row][col] = 255
    
    paths = PriorityQueue()
    seen = PriorityQueue()
    h=heuristic(pos_x, pos_y, goal_x, goal_y)
    paths.put((h, ([(pos_x, pos_y, theta1, theta2)], 0)))
    path = []
    visited = [(theta1, theta2)]
    init_time=time.time()
    
    while not paths.empty():
        path=paths.get()
        h=path[0]
        posAry, dist=path[1]
        pos_x, pos_y, theta1, theta2=posAry[0]
        
        if pos_x==goal_x and pos_y==goal_y:
            soln_time=int(time.time()-init_time)
            print("found solution in ", soln_time//60, "minutes and ", soln_time%60, " seconds")
            print(h, posAry, heuristic(pos_x, pos_y, goal_x, goal_y))
            break

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_theta1=(theta1+10*i)%360
                new_theta2=(theta2+10*j)%360

                if (i!=0 or j!=0) and (i==0 or j==0) and new_theta1>=0 and new_theta1<=180:
                    new_x=len_1*math.cos(math.pi*new_theta1/180)+len_2*math.cos(math.pi*(new_theta2)/180)
                    new_y=len_1*math.sin(math.pi*new_theta1/180)+len_2*math.sin(math.pi*(new_theta2)/180)

                    if ((new_x, new_y, new_theta1, new_theta2) not in posAry) and ((new_theta1, new_theta2) not in visited):
                        newH = heuristic(new_x, new_y, goal_x, goal_y)+math.sqrt((new_x-pos_x)**2+(new_y-pos_y)**2)+dist
                        new_dist=math.sqrt((new_x-pos_x)**2+(new_y-pos_y)**2)+dist
                        canPut=True

                        for obstacle in obstacles:
                            if obstacle.clash(new_x, new_y):
                                canPut=False
                                break

                        if canPut: 
                            paths.put((newH, ([(new_x, new_y, new_theta1, new_theta2)]+posAry, new_dist)))
                            visited += [(new_theta1, new_theta2)]

        seen.put((heuristic(pos_x, pos_y, goal_x, goal_y)+0.05*len(posAry), (posAry))) #switch to 0.05
    
    if pos_x != goal_x or pos_y != goal_y:
        fin_path = seen.get()
        x, y, theta1, theta2 = fin_path[1][0]
        #print(fin_path[0], fin_path[1], heuristic(x, y, goal_x, goal_y), len(fin_path[1]))
        #print(fin_path[0], heuristic(x, y, goal_x, goal_y), len(fin_path[1]))
        soln_time = int(time.time()-init_time)
        posAry=fin_path[1]    
    
    count=0
    soln=[]

    for term in posAry:
        x, y, theta1, theta2 = term
        x_coord = x*frac_size
        y_coord = y*frac_size
        img[max_row-int(y_coord)][center_col+int(x_coord)][0] = 128+count
        count+=1
        soln+=[(theta1, theta2)]


    
    print(soln[::-1])
    print("\n\n")
 
    '''plt.imshow(img)
    plt.xlabel("x (1/8 inches)")
    plt.ylabel("y (1/8 inches)")
    ax = plt.gca()
    ax.set_xticks(numpy.arange(0, 113, 8))
    ax.set_yticks(numpy.arange(0, 65, 8))
    ax.set_xticklabels(numpy.arange(-7, 8, 1))
    ax.set_yticklabels(numpy.arange(8, -1, -1))
    plt.show()'''

    return posAry[0], soln[::-1]
