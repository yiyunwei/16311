# import socket

# HOST = ''                 # Symbolic name meaning all available interfaces
# PORT = 5050              # Arbitrary non-privileged port
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen(1)
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data: break
#             conn.sendall(data)

import brickpi3, time
import socket
import subprocess

BP = brickpi3.BrickPi3()
print(BP.get_voltage_battery())

leftmotor = BP.PORT_D
rightmotor = BP.PORT_A
armmotor = BP.PORT_C

command = "raspistill -v -o test.jpg | python3 ./threshold.py"

s=socket.socket()       # arguments(IPV4, TCP)
HOST1=''        # IPV4 address of the server

PORT=7070               # use any port between 4000 and 65000
s.bind((HOST1,PORT))    # assigns the socket with an address
s.listen(5)             # accept no. of incoming connections

def is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

while True:
    clientsocket, address = s.accept()          # stores the socket details in 2 variables
    print("Connection from ", address, " has been established")
    clientsocket.send(bytes("Welcome to the server, \nWhat is your name?",'utf-8'))     # encodes a string into bytes and sends it to client
    name=clientsocket.recv(10)          # recieves a packet of 10 bytes from the client ie the name
    name=name.decode('utf-8')           # decodes the bytes into string format
    print("\nConnecting to ",name," . . .")
    count=0                             # while counter
    while True:
        count+=1
        LETTER=clientsocket.recv(1)                                 # recieves an alphabet whose ASCII value is the size of the message 
        SIZE=ord(LETTER.decode('utf-8'))                            # ord() returns the ASCII value of a character
        msg=clientsocket.recv(SIZE)                                 # recieving the actual msg
        #print(msg)
        instr = msg.decode('utf-8')
        x = instr.split(" ")

        if len(x)==3:
            b = x[0]
            l = x[1]
            r = x[2]

            if (count%1000 == 0) and is_num(l) and is_num(r):
                #print(x)
                if(b == "X"):
                    BP.set_motor_power(rightmotor, 0)
                    BP.set_motor_power(leftmotor, 0)
                    BP.set_motor_power(armmotor, 0)
                    subprocess.run(command, shell = True, executable="/bin/bash")
                elif(b == "[]"):
                    BP.set_motor_power(rightmotor, 0)
                    BP.set_motor_power(leftmotor, 0)
                    if (l != None):
                        BP.set_motor_power(armmotor, 100*float(l))
                else:
                    BP.set_motor_power(rightmotor, 100*float(r))
                    BP.set_motor_power(leftmotor, 100*float(l))
                    BP.set_motor_power(armmotor, 0)
        
        # BLET = clientsocket.recv(1)
        # BSIZE= ord(BLET.decode('utf-8'))
        # button = clientsocket.recv(BSIZE)
        # b = button.decode('utf-8')
        
        # LLET = clientsocket.recv(1)
        # LSIZE = ord(LLET.decode('utf-8'))
        # left = clientsocket.recv(LSIZE)
        # l = left.decode('utf-8')

        # RLET = clientsocket.recv(1)
        # RSIZE = ord(RLET.decode('utf-8'))
        # right = clientsocket.recv(RSIZE)
        # r = right.decode('utf-8')


        #if count%1000==0:           # preventing print in each loop
            #print("b: ", b, " l: ", l, " r: ", r, "\n")

    clientsocket.close()                              # close socket connection after use
