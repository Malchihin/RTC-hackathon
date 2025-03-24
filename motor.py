import RPi.GPIO as GPIO
import time

motor_pin1 = 17  
motor_pin2 = 27  

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin1, GPIO.OUT)
GPIO.setup(motor_pin2, GPIO.OUT)

def forward():
    GPIO.output(motor_pin1, GPIO.HIGH)
    GPIO.output(motor_pin2, GPIO.LOW)

def backward():
    GPIO.output(motor_pin1, GPIO.LOW)
    GPIO.output(motor_pin2, GPIO.HIGH)

def stop():
    GPIO.output(motor_pin1, GPIO.LOW)
    GPIO.output(motor_pin2, GPIO.LOW)

try:

    forward()
    time.sleep(2) 
    stop()
    time.sleep(1) 
    backward()
    time.sleep(2)  
    stop()

finally:
    GPIO.cleanup()
