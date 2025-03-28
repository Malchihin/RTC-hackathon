from picamera2 import Picamera2, Preview
from time import sleep
import cv2
import cv2.aruco
import RPi.GPIO as GPIO
import time

#camera = Picamera2()

#camera.start_preview()

#camera.start()

#arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
#arucoParam = cv2.aruco.DetectorParameters()
#arucoDetect = cv2.aruco.ArucoDetector(arucoDict, arucoParam)

#robotID = 1
#points = [[0, 0]]


motor_pin1 = 17
motor_pin2 = 27

servo_pi_motor = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin1, GPIO.OUT)
GPIO.setup(motor_pin2, GPIO.OUT)

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pi_motor, GPIO.OUT)
pwm = GPIO.PWM(servo_pi_motor, 50)
pwm.start(0)

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

def set_angle(angle):
    """Установить угол поворота сервопривода."""
    duty_cycle = 2 + (angle / 18)  # Преобразование угла в рабочий цикл
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)

try:
    while True:
       # try:
           # img = camera.capture_array()
            #markerCorners, markerIDs, _ = arucoDetect.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
            #if markerIDs is not None:
                #for i, markerID in enumerate(markerIDs):
                   # if markerID[0] == robotID:
                       # corners = markerCorners[i][0]
                        #corners_x = int((corners[0][0] + corners[1][0] + corners[2][0] + corners[3][0]) / 4)
                        #corners_y = int((corners[0][1] + corners[1][1] + corners[2][1] + corners[3][1]) / 4)
                        #print(f"Marker ID: {markerID[0]}, Center: ({corners_x}, {corners_y})")
            #cv2.imshow("Image", img)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
               # break
        #except:points.clear()
	
        #set_angle(25)
        #time.sleep(0.5)
        
        forward()
        print(1)
        time.sleep(0.5)


        backward()
        #print(2)
        time.sleep(0.5)
	 
        set_angle(25)   

        #if markerID is not None:
           # if markerID == robotID:
               # stop()
                #print(2)
                #time.sleep(1)
        
    
except KeyboardInterrupt:
    GPIO.cleanup()


pwm.stop()
GPIO.cleanup()
