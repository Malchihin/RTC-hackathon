import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
for pin in [4, 5, 6]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Включить датчик