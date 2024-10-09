from __future__ import print_function 
from __future__ import division
import brickpi3, time
import pygame

BP = brickpi3.BrickPi3()
print(BP.get_voltage_battery())

pygame.init()

leftmotor = BP.PORT_D
rightmotor = BP.PORT_A
armmotor = BP.PORT_C

NUMAXES = 4
LEFTX = 0
LEFTY = 1
RIGHTX = 2
RIGHTY = 3
# left = -1, right = 1, up = -1, down = 1

NUMBUTTONS = 13
SQUARE = 0
X = 1
O = 2
TRIANGLE = 3
L1 = 4
R1 = 5
L2 = 6
R2 = 7
LEFTKNOB = 10
RIGHTKNOB = 11

NUMHATS = 1
HAT = 0
# hat = (x, y) (x = left (-1) + right (1), y = up (1) + down (-1))

def main():
    joysticks = {}

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")


        for i in range(NUMAXES):
            axis = joystick.get_axis(i)
            
            text_print.tprint(screen, f"Axis {i} value: {axis:>6.3f}")
        
        for i in range(buttons):
            button = joystick.get_button(i)
            text_print.tprint(screen, f"Button {i:>2} value: {button}")

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            text_print.tprint(screen, f"Hat {i} value: {str(hat)}")


if __name__ == "__main__":
    main()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()