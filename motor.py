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

    motor1_pwm1 = GPIO.PWM(motor_pin1, 100)
    motor1_pwm2 = GPIO.PWM(motor_pin2, 100)

    motor2_pwm1 = GPIO.PWM(motor2_pin1, 100)
    motor2_pwm2 = GPIO.PWM(motor2_pin2, 100)

    GPIO.setup(servo_pi_motor, GPIO.OUT)

    pwm = GPIO.PWM(servo_pi_motor, 50)
    pwm.start(0)

    motor_pin1.start(0)
    motor1_pwm2.start(0)

    motor_pin1.start(0)
    motor1_pwm2.start(0)

    
    def forward():
        print("Forward")
        motor1_pwm1.ChangeDutyCycle(100)
        motor1_pwm2.ChangeDutyCycle(0)
        motor2_pwm1.ChangeDutyCycle(100)
        motor2_pwm2.ChangeDutyCycle(0)
    
    def backward():
        print("Backward")
        motor1_pwm1.ChangeDutyCycle(0)
        motor1_pwm2.ChangeDutyCycle(100)
        motor2_pwm1.ChangeDutyCycle(0)
        motor2_pwm2.ChangeDutyCycle(100)
    
    def stop():
        print("Stop")
        motor1_pwm1.ChangeDutyCycle(0)
        motor1_pwm2.ChangeDutyCycle(0)
        motor2_pwm1.ChangeDutyCycle(0)
        motor2_pwm2.ChangeDutyCycle(0)

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

    motor_pin1.stop()
    motor_pin2.stop()

    motor2_pin1.stop()
    motor2_pin2.stop()

    GPIO.cleanup()
