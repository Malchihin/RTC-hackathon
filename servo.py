import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
servo = GPIO.PWM(18,50)
servo.start(0)
print(1)