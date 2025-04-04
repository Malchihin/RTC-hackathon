import RPi.GPIO as GPIO
import time

# Определение пинов
motor_pin1 = 17
motor_pin2 = 27
motor2_pin1 = 23
motor2_pin2 = 24
servo_pi_motor = 18

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin1, GPIO.OUT)
GPIO.setup(motor_pin2, GPIO.OUT)
GPIO.setup(motor2_pin1, GPIO.OUT)
GPIO.setup(motor2_pin2, GPIO.OUT)
GPIO.setup(servo_pi_motor, GPIO.OUT)

# Создание объектов PWM
motor1_pwm1 = GPIO.PWM(motor_pin1, 50)
motor1_pwm2 = GPIO.PWM(motor_pin2, 50)
motor2_pwm1 = GPIO.PWM(motor2_pin1, 50)
motor2_pwm2 = GPIO.PWM(motor2_pin2, 50)
pwm = GPIO.PWM(servo_pi_motor, 50)

# Запуск PWM
motor1_pwm1.start(0)
motor1_pwm2.start(0)
motor2_pwm1.start(0)
motor2_pwm2.start(0)
pwm.start(0)

def forward():
    print("Forward")
    motor1_pwm1.ChangeDutyCycle(15)
    motor1_pwm2.ChangeDutyCycle(0)
    motor2_pwm1.ChangeDutyCycle(15)
    motor2_pwm2.ChangeDutyCycle(0)

def backward():
    print("Backward")
    motor1_pwm1.ChangeDutyCycle(0)
    motor1_pwm2.ChangeDutyCycle(15)
    motor2_pwm1.ChangeDutyCycle(0)
    motor2_pwm2.ChangeDutyCycle(15)

def stop():
    print("Stop")
    motor1_pwm1.ChangeDutyCycle(0)
    motor1_pwm2.ChangeDutyCycle(0)
    motor2_pwm1.ChangeDutyCycle(0)
    motor2_pwm2.ChangeDutyCycle(0)

def right():
    print("right")
    motor1_pwm1.ChangeDutyCycle(15)
    motor1_pwm2.ChangeDutyCycle(0)
    motor2_pwm1.ChangeDutyCycle(0)
    motor2_pwm2.ChangeDutyCycle(15)

def left():
    print("left")
    motor1_pwm1.ChangeDutyCycle(0)
    motor1_pwm2.ChangeDutyCycle(15)
    motor2_pwm1.ChangeDutyCycle(15)
    motor2_pwm2.ChangeDutyCycle(0)

def set_angle(angle):
    """Установить угол поворота сервопривода."""
    duty_cycle = 2 + (angle / 18)  # Преобразование угла в рабочий цикл
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)

try:
    while True:

        set_angle(0)

        forward()
        time.sleep(5)

        backward()
        time.sleep(5)

        right()
        time.sleep(5)

        left()
        time.sleep(5)

except KeyboardInterrupt:
    pass

finally:
    # Остановка PWM и очистка GPIO
    motor1_pwm1.stop()
    motor1_pwm2.stop()
    motor2_pwm1.stop()
    motor2_pwm2.stop()
    pwm.stop()
    GPIO.cleanup()
