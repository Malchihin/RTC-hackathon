import RPi.GPIO as GPIO
import time

# Настройки пинов
IA = 17  # Пин для управления IA
IB = 27  # Пин для управления IB

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IA, GPIO.OUT)
GPIO.setup(IB, GPIO.OUT)

def forward():
    GPIO.output(IA, GPIO.HIGH)
    GPIO.output(IB, GPIO.LOW)

def backward():
    GPIO.output(IA, GPIO.LOW)
    GPIO.output(IB, GPIO.HIGH)

def stop():
    GPIO.output(IA, GPIO.LOW)
    GPIO.output(IB, GPIO.LOW)

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
