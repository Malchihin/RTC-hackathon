#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import VL53L0X
import smbus2

# Настройка пинов для двигателей и сервопривода
MOTOR1_PIN1 = 17
MOTOR1_PIN2 = 27
MOTOR2_PIN1 = 23
MOTOR2_PIN2 = 24
SERVO_PIN = 18

# Пины для управления датчиками VL53L0X
SENSOR1_XSHUT = 4
SENSOR2_XSHUT = 5
SENSOR3_XSHUT = 6

class RobotController:
    def __init__(self):
        # Инициализация GPIO
        GPIO.setmode(GPIO.BCM)
        self.setup_motors()
        self.setup_servo()
        self.setup_sensors()
        
    def setup_motors(self):
        """Настройка пинов для двигателей"""
        GPIO.setup(MOTOR1_PIN1, GPIO.OUT)
        GPIO.setup(MOTOR1_PIN2, GPIO.OUT)
        GPIO.setup(MOTOR2_PIN1, GPIO.OUT)
        GPIO.setup(MOTOR2_PIN2, GPIO.OUT)
        
        # Создание PWM объектов для двигателей
        self.motor1_pwm1 = GPIO.PWM(MOTOR1_PIN1, 50)
        self.motor1_pwm2 = GPIO.PWM(MOTOR1_PIN2, 50)
        self.motor2_pwm1 = GPIO.PWM(MOTOR2_PIN1, 50)
        self.motor2_pwm2 = GPIO.PWM(MOTOR2_PIN2, 50)
        
        # Запуск PWM
        self.motor1_pwm1.start(0)
        self.motor1_pwm2.start(0)
        self.motor2_pwm1.start(0)
        self.motor2_pwm2.start(0)
    
    def setup_servo(self):
        """Настройка сервопривода"""
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.servo_pwm = GPIO.PWM(SERVO_PIN, 50)
        self.servo_pwm.start(0)
    
    def setup_sensors(self):
        """Инициализация трех датчиков VL53L0X"""
        GPIO.setup(SENSOR1_XSHUT, GPIO.OUT)
        GPIO.setup(SENSOR2_XSHUT, GPIO.OUT)
        GPIO.setup(SENSOR3_XSHUT, GPIO.OUT)
        
        # Выключаем все датчики
        GPIO.output(SENSOR1_XSHUT, GPIO.LOW)
        GPIO.output(SENSOR2_XSHUT, GPIO.LOW)
        GPIO.output(SENSOR3_XSHUT, GPIO.LOW)
        time.sleep(0.5)
        
        # Инициализируем датчики с разными адресами
        self.sensors = []
        self.init_sensor(SENSOR1_XSHUT, 0x29)
        self.init_sensor(SENSOR2_XSHUT, 0x30)
        self.init_sensor(SENSOR3_XSHUT, 0x31)
    
    def init_sensor(self, xshut_pin, new_address):
        """Инициализация одного датчика"""
        GPIO.output(xshut_pin, GPIO.HIGH)
        time.sleep(0.1)
        
        bus = smbus2.SMBus(1)
        sensor = VL53L0X.VL53L0X(i2c_bus=bus)
        sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        
        # Меняем адрес датчика
        sensor.change_address(new_address)
        sensor.stop_ranging()
        bus.close()
        
        # Перезапускаем с новым адресом
        bus = smbus2.SMBus(1)
        sensor = VL53L0X.VL53L0X(address=new_address, i2c_bus=bus)
        sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        self.sensors.append(sensor)
        
        print(f"Датчик на пине {xshut_pin} инициализирован с адресом 0x{new_address:02X}")
    
    def get_distances(self):
        """Получение расстояний от всех датчиков"""
        distances = []
        for sensor in self.sensors:
            distance = sensor.get_distance()
            distances.append(distance if distance > 0 else None)
        return distances
    
    def set_servo_angle(self, angle):
        """Установка угла сервопривода"""
        duty_cycle = 2 + (angle / 18)
        self.servo_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.3)
        self.servo_pwm.ChangeDutyCycle(0)  # Останавливаем PWM для сервопривода
    
    def move_forward(self, speed=15):
        """Движение вперед"""
        self.motor1_pwm1.ChangeDutyCycle(speed)
        self.motor1_pwm2.ChangeDutyCycle(0)
        self.motor2_pwm1.ChangeDutyCycle(speed)
        self.motor2_pwm2.ChangeDutyCycle(0)
    
    def move_backward(self, speed=15):
        """Движение назад"""
        self.motor1_pwm1.ChangeDutyCycle(0)
        self.motor1_pwm2.ChangeDutyCycle(speed)
        self.motor2_pwm1.ChangeDutyCycle(0)
        self.motor2_pwm2.ChangeDutyCycle(speed)
    
    def turn_right(self, speed=15):
        """Поворот направо"""
        self.motor1_pwm1.ChangeDutyCycle(speed)
        self.motor1_pwm2.ChangeDutyCycle(0)
        self.motor2_pwm1.ChangeDutyCycle(0)
        self.motor2_pwm2.ChangeDutyCycle(speed)
    
    def turn_left(self, speed=15):
        """Поворот налево"""
        self.motor1_pwm1.ChangeDutyCycle(0)
        self.motor1_pwm2.ChangeDutyCycle(speed)
        self.motor2_pwm1.ChangeDutyCycle(speed)
        self.motor2_pwm2.ChangeDutyCycle(0)
    
    def stop(self):
        """Остановка всех двигателей"""
        self.motor1_pwm1.ChangeDutyCycle(0)
        self.motor1_pwm2.ChangeDutyCycle(0)
        self.motor2_pwm1.ChangeDutyCycle(0)
        self.motor2_pwm2.ChangeDutyCycle(0)
    
    def avoid_obstacles(self):
        """Автоматическое избегание препятствий"""
        while True:
            distances = self.get_distances()
            print(f"Расстояния: {distances} мм")
            
            if all(d is None or d > 300 for d in distances):
                self.move_forward()
            elif distances[0] is not None and distances[0] < 300:
                self.stop()
                time.sleep(0.5)
                self.set_servo_angle(90)
                time.sleep(0.5)
                right_dist = self.get_distances()[1]
                left_dist = self.get_distances()[2]
                
                if right_dist is not None and left_dist is not None:
                    if right_dist > left_dist:
                        self.turn_right()
                        time.sleep(1)
                    else:
                        self.turn_left()
                        time.sleep(1)
                self.set_servo_angle(0)
            time.sleep(0.1)
    
    def cleanup(self):
        """Очистка ресурсов"""
        self.stop()
        for sensor in self.sensors:
            sensor.stop_ranging()
        self.servo_pwm.stop()
        self.motor1_pwm1.stop()
        self.motor1_pwm2.stop()
        self.motor2_pwm1.stop()
        self.motor2_pwm2.stop()
        GPIO.cleanup()
        print("Ресурсы освобождены")

def main():
    try:
        robot = RobotController()
        
        ## Демонстрационный режим
        #print("Демонстрация работы робота")
        #robot.set_servo_angle(0)
        #
        #print("Движение вперед")
        #robot.move_forward()
        #time.sleep(2)
        #
        #print("Движение назад")
        #robot.move_backward()
        #time.sleep(2)
        #
        #print("Поворот направо")
        #robot.turn_right()
        #time.sleep(2)
        #
        #print("Поворот налево")
        #robot.turn_left()
        #time.sleep(2)
        #
        #robot.stop()
        
        # Режим автоматического избегания препятствий
        print("Запуск режима избегания препятствий")
        robot.avoid_obstacles()
        
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
    finally:
        robot.cleanup()

if __name__ == "__main__":
    main()
