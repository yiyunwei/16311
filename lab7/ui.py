from __future__ import print_function 
from __future__ import division
import brickpi3, time
import curses
import subprocess


BP = brickpi3.BrickPi3()
print(BP.get_voltage_battery())

leftmotor = BP.PORT_D
rightmotor = BP.PORT_A
armmotor = BP.PORT_C
command = "raspistill -v -o test.jpg | python3 ./threshold.py"

def c_main(stdscr):
    t=time.time()
    while True:
        try:
            char = stdscr.get_wch()
            if char == 'd':
                stdscr.addstr("left")
                BP.set_motor_power(rightmotor, -40)
                BP.set_motor_power(leftmotor, 40)
                t=time.time()
            elif char == 'W':
                stdscr.addstr("fast forward") # toward weights
                BP.set_motor_power(rightmotor, 100)
                BP.set_motor_power(leftmotor, 100)
                t=time.time()
            elif char == 'w':
                stdscr.addstr("slow forward") # toward weights
                BP.set_motor_power(rightmotor, 40)
                BP.set_motor_power(leftmotor, 40)
                t=time.time()
            elif char == 'S':
                stdscr.addstr("fast backward") # toward arm
                BP.set_motor_power(rightmotor, -80)
                BP.set_motor_power(leftmotor, -80)
                t=time.time()
            elif char == 's':
                stdscr.addstr("backward") # toward arm
                BP.set_motor_power(rightmotor, -40)
                BP.set_motor_power(leftmotor, -40)
                t=time.time()
            elif char == 'a':
                stdscr.addstr("right")
                BP.set_motor_power(rightmotor, 40)
                BP.set_motor_power(leftmotor, -40)
                t=time.time()
            elif char == 'j':
                stdscr.addstr("raise")
                BP.set_motor_power(armmotor, 100)
                t=time.time()
            elif char == 'k':
                stdscr.addstr("lower")
                BP.set_motor_power(armmotor, -100)
                t=time.time()
            elif char == 'e':
                stdscr.addstr("left wheel")
                BP.set_motor_power(leftmotor, 0)
                BP.set_motor_power(rightmotor, -100)
                t=time.time()
            elif char == 'q':
                stdscr.addstr("right wheel")
                BP.set_motor_power(leftmotor, -100)
                BP.set_motor_power(rightmotor, 0)
                t=time.time()
            elif char == 'm':
                stdscr.addstr("photo")
                #TEST THIS
                subprocess.run(command, shell = True, executable="/bin/bash")
            elif char == ' ' or time.time()-t>3:
                stdscr.addstr("stop")
                BP.set_motor_power(rightmotor, 0)
                BP.set_motor_power(leftmotor, 0)
                BP.set_motor_power(armmotor, 0)
                t=time.time()
        except KeyboardInterrupt:
            BP.set_motor_power(leftmotor, 0)
            BP.set_motor_power(rightmotor, 0)
            BP.set_motor_power(armmotor, 0)
            BP.reset_all()
            break

def main():
    curses.wrapper(c_main)
    return 0

if __name__ == '__main__':
    exit(main())