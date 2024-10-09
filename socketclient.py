#yiyun ip address 172.26.27.162 (when on cmu secure)
#pi ip address 172.26.229.46

# import socket
# import pygame

# HOST = '172.26.229.46'    # The remote host
# PORT = 5050              # The same port as used by the server

# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"

# pygame.init()
# #pygame.display.set_mode((200, 200))
# #pygame.display.set_caption("Joystick example")

# done = False
# #while not done:
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     #s.sendall(b'Hello, world')

#     joysticks = {}
#     done = False
#     while not done:
#         s.sendall(b'Hello, world')
        # for event in pygame.event.get():
        #     #print(event)
        #     #s.sendall(b'Hello, world')
        #     if event.type == pygame.QUIT:
        #         done = True  # Flag that we are done so we exit this loop.
        #         #s.sendall(b'quitter')

            # if event.type == pygame.JOYBUTTONDOWN:
            #     print("button down")
            #     #s.sendall(b'Joystick button pressed.')

            # if event.type == pygame.JOYBUTTONUP:
            #     print("button up")
            #     #s.sendall(b'Joystick button released.')

            #             # Handle hotplugging
            # if event.type == pygame.JOYDEVICEADDED:
            #     # This event will be generated when the program starts for every
            #     # joystick, filling up the list without needing to create them manually.
            #     joy = pygame.joystick.Joystick(event.device_index)
            #     joysticks[joy.get_instance_id()] = joy
            #     print(f"Joystick {joy.get_instance_id()} connencted")

            # if event.type == pygame.JOYDEVICEREMOVED:
            #     del joysticks[event.instance_id]
            #     print(f"Joystick {event.instance_id} disconnected")
            
            #else:
                #s.sendall(b'')

        # data = s.recv(1024)
        # print('Received', repr(data))

# Echo client program
# import socket

# HOST = '172.26.229.46'    # The remote host
# PORT = 5050              # The same port as used by the server
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     while True:
#         s.sendall(b'Hello, world')
#         data = s.recv(1024)
#         print('Received', repr(data))

import socket
import pygame as pg
import time

c=socket.socket()                       # arguementss (IPV4, TCP)
HOST1='172.26.229.46'                    # IPV4 address of the server
PORT=7070
c.connect((HOST1,PORT))                 # connects client to an address
msg=c.recv(64)                          # recieves a packet of 64 bytes from server
print(msg.decode('utf-8'))              # decodes bytes into string

name=input()
c.send(bytes(name,'utf-8'))             # encodes name string to bytes and sends to server

pg.init()                               # initiates pygame window

screen = pg.display.set_mode((200,200),pg.RESIZABLE)        # all operations must be performed on pg screen
done = False
pg.joystick.init()                      
if(pg.joystick.get_count()!=0):         # checks whether a joystick is connected
    joystick = pg.joystick.Joystick(0)
    print(joystick)
    joystick.init()

while not done:
    button="None "      # deafult msg
    lax = "0 "
    rax = "0"
    if(pg.joystick.get_count()!=0):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
        axis1 = joystick.get_axis( 1 ) # gets front and back value from left stick of joystick
        axis1 = int(-100*axis1)        # converts 8 point float value to 0-100 range
        axis0 = joystick.get_axis( 0 ) # gets left/ back value from left stick
        axis0 = int(100*axis0)
        axis2 = joystick.get_axis( 2 ) # gets left and right trigger values
        axis2 = int(100*axis2)
        axis3 = joystick.get_axis( 3 ) # gets left and right trigger values
        axis3 = int(-100*axis3)

        Sq = joystick.get_button( 0 )   # following buttons return bool value if (not) pressed
        X = joystick.get_button( 1 )
        O = joystick.get_button( 2 )
        Tr = joystick.get_button( 3 )
        L1 = joystick.get_button( 4 )
        R1 = joystick.get_button( 5 )
        L2 = joystick.get_button( 6 )
        R2 = joystick.get_button( 7 )

        START = joystick.get_button( 9 )
        keys = pg.key.get_pressed()
        if Sq == 1:
            button="[] "      # button is the message to be sent
        if X == 1:
            button="X "
        if O == 1:
            button="O "      # button takes values accordingly
        if Tr == 1:
            button="<| "
        if L1 == 1:
            button="L1 "
        if R1 == 1:
            button="R1 "
        if L2 == 1:
            button="L2 "
        if R2 == 1:
            button="R2 "

        if START==1:                   # press START button on joystick to QUIT
            done = True         
        # if axis1 < -15:               # ignoring small values
        #     lax=("LBack: " + str( -axis1/100 ) )  # we must keep button completely a string to encode into bytes
        # if axis1 > 15:
        #     lax=("LFor: " + str( axis1/100 ) )
        # if axis0 < -25:
        #     lax=("LLeft: " + str( -axis0/100 ) )
        # if axis0 > 25:
        #     lax=("LRight: " + str( axis0/100 ) )
        # if axis2 < -25:
        #     rax=("RLeft: " + str( -axis2/100 ) )
        # if axis2 > 25:
        #     rax=("RRight: " + str( axis2/100 ) )
        # if axis3 < -15:               # ignoring small values
        #     rax=("RBack: " + str( -axis3/100 ) )  # we must keep button completely a string to encode into bytes
        # if axis3 > 15:
        #     rax=("RFor: " + str( axis3/100 ) )
        
        if abs(axis1) > 15:               # ignoring small values
            lax=(str( axis1/100 ) + " ")  # we must keep button completely a string to encode into bytes
        if abs(axis3) > 15:
            rax=(str( axis3/100))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:  # arrow keys on keyboard upon pressing
        button="KEY LEFT"
    elif keys[pg.K_RIGHT]: 
        button="KEY RIGHT"
    elif keys[pg.K_UP]:  
        button="KEY UP"
    elif keys[pg.K_DOWN]: 
        button="KEY DOWN"
    elif keys[pg.K_ESCAPE]:  # press ESC to QUIT
        done=True

    HEADER = chr(len(button) + len(lax) + len(rax))
    c.send(bytes(HEADER,'utf-8'))
    c.send(bytes(button + lax + rax, 'utf-8'))

    # BHEAD=chr(len(button))         # chr() returns the character whose ASCII value is passed to it
    #                                 # HEADER stores the character whose ASCII value is length of button
    # LHEAD=chr(len(lax))
    # RHEAD=chr(len(rax))
    
    # c.send(bytes(BHEAD,'utf-8'))   # first we send HEADER so the server knows the length of button to recieve
    # c.send(bytes(button,'utf-8'))   # sending button to server
    #time.sleep(0.1)
    # c.send(bytes(LHEAD,'utf-8'))
    # c.send(bytes(lax,'utf-8'))
    #time.sleep(0.1)
    # c.send(bytes(RHEAD,'utf-8'))
    # c.send(bytes(rax,'utf-8'))
    #time.sleep(0.1)

pg.quit()  # quit pygame window