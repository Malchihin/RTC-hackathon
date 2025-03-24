import RPi.GPIO as GPIO
import time

motor_pin1 = 17
motor_pin2 = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin1, GPIO.OUT)
GPIO.setup(motor_pin2, GPIO.OUT)

def forward():
    print(1)
    GPIO.output(motor_pin1, GPIO.HIGH)
    GPIO.output(motor_pin2, GPIO.LOW)

def backward():
    print(2)
    GPIO.output(motor_pin1, GPIO.LOW)
    GPIO.output(motor_pin2, GPIO.HIGH)

def stop():
    print(2)
    GPIO.output(motor_pin1, GPIO.LOW)
    GPIO.output(motor_pin2, GPIO.LOW)

while True:
    forward()
    time.sleep(2)
    stop()
    time.sleep(1)
    backward()
    time.sleep(2)
    stop()

    
