import brickpi3
import RPi.GPIO as GPIO
import time

light = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
led_pwm = GPIO.PWM(light,1000)
led_pwm.start(0)

while True:
    for duty in range(101):
        led_pwm.ChangeDutyCycle(duty)
        time.sleep(0.01)
    time.sleep(0.5)
    for duty in range(100,-1,-1):
        led_pwm.ChangeDutyCycle(duty)
        time.sleep(0.01)
    time.sleep(0.5)



GPIO.cleanup()