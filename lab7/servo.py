import brickpi3
import RPi.GPIO as GPIO
import time

servo = 12 #need to confirm
dcgearbox = 23 #need to confirm
dutycycle = 1

GPIO.setmode(GPIO.BOARD)

GPIO.setup(servo, GPIO.OUT)
GPIO.setup(dcgearbox, GPIO.OUT)

# GPIO.output(dcgearbox, GPIO.HIGH)
# time.sleep(5)
# GPIO.output(dcgearbox, GPIO.LOW)

# p = GPIO.PWM(servo, 0.5)
# p.start(1)


# for i in range(5):
    
#     #p.start(dutycycle)
#     GPIO.output(dcgearbox, GPIO.HIGH)
#     print("hi")
#     time.sleep(1)
#     GPIO.output(dcgearbox, GPIO.LOW)
#     #p.stop()
GPIO.cleanup()