from picamera2 import Picamera2, Preview
from time import sleep
import cv2
import cv2.aruco
import RPi.GPIO as GPIO

motor_pin = 17
motor_pin2 = 27
servo_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin, GPIO.OUT)
GPIO.setup(motor_pin2, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)

camera = Picamera2()
camera.start_preview()
camera.start()

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
arucoParam = cv2.aruco.DetectorParameters()
arucoDetect = cv2.aruco.ArucoDetector(arucoDict, arucoParam)

def straight():
    GPIO.output(motor_pin, GPIO.HIGH)
    GPIO.output(motor_pin2, GPIO.LOW)

def stop():
    GPIO.output(motor_pin, GPIO.LOW)
    GPIO.output(motor_pin2, GPIO.LOW)

def turn_servo(angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)