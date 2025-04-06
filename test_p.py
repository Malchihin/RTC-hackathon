import RPi.GPIO as GPIO
import time

# Отключаем предупреждения о повторном использовании пинов
GPIO.setwarnings(False)

# Настройка режима нумерации пинов
GPIO.setmode(GPIO.BCM)

# Пины для управления датчиками
SENSOR_PINS = [4, 5, 6]  # GPIO4, GPIO5, GPIO6

try:
    # Инициализация пинов
    for pin in SENSOR_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)  # Включаем датчики
    
    print("Все датчики активированы. Проверьте i2cdetect:")
    print("Откройте новое окно терминала и выполните:")
    print("sudo i2cdetect -y 1")
    print("Ожидание 30 секунд...")
    
    time.sleep(30)

finally:
    # Всегда очищаем настройки GPIO при завершении
    GPIO.cleanup()
    print("Ресурсы GPIO освобождены")
