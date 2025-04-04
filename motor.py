import RPi.GPIO as GPIO
import time

motor_pin1 = 17
motor_pin2 = 27

motor2_pin1 = 23
motor2_pin2 = 24

servo_pi_motor = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin1, GPIO.OUT)
GPIO.setup(motor_pin2, GPIO.OUT)

GPIO.setup(motor2_pin1, GPIO.OUT)
GPIO.setup(motor2_pin2, GPIO.OUT)

GPIO.setup(servo_pi_motor, GPIO.OUT)

pwm = GPIO.PWM(servo_pi_motor, 50)
pwm.start(0)

def forward():
    print(1)
    GPIO.output(motor_pin1, GPIO.HIGH)
    GPIO.output(motor_pin2, GPIO.LOW)

    GPIO.output(motor2_pin1, GPIO.HIGH)
    GPIO.output(motor2_pin2, GPIO.LOW)

def backward():
    print(2)
    GPIO.output(motor_pin1, GPIO.LOW)
    GPIO.output(motor_pin2, GPIO.HIGH)

    GPIO.output(motor2_pin1, GPIO.LOW)
    GPIO.output(motor2_pin2, GPIO.HIGH)

def stop():
    print(2)
    GPIO.output(motor_pin1, GPIO.LOW)
    GPIO.output(motor_pin2, GPIO.LOW)

    GPIO.output(motor2_pin1, GPIO.LOW)
    GPIO.output(motor2_pin2, GPIO.LOW)

def set_angle(angle):
    """Установить угол поворота сервопривода."""
    duty_cycle = 2 + (angle / 18)  # Преобразование угла в рабочий цикл
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)

try:
    while True:
        set_angle(25)
        time.sleep(0.5)

        forward()
        print(1)
        time.sleep(0.5)

        backward()
        print(2)
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()

pwm.stop()
GPIO.cleanup()
