import RPi.GPIO as GPIO
import time

# Укажите номер GPIO-порта, к которому подключен сервопривод
SERVO_PIN = 18

# Установите режим нумерации пинов (BCM или BOARD)
GPIO.setmode(GPIO.BCM)

# Настройте пин как выход
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Создайте объект PWM с частотой 50 Гц
pwm = GPIO.PWM(SERVO_PIN, 50)

# Начальная установка PWM
pwm.start(0)

def set_angle(angle):
    """Установить угол поворота сервопривода."""
    duty_cycle = 2 + (angle / 18)  # Преобразование угла в рабочий цикл
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)  # Дать время сервоприводу достичь позиции

try:
    while True:
        # Установите угол 0 градусов
        set_angle(0)
        time.sleep(1)

        # Установите угол 90 градусов
        set_angle(90)
        time.sleep(1)

        # Установите угол 180 градусов
        set_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    # Остановите PWM и очистите настройки GPIO при завершении программы
    pwm.stop()
    GPIO.cleanup()
