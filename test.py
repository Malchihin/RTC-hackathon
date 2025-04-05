import RPi.GPIO as GPIO
import time
import VL53L0X
import smbus2

def setup_sensors(self):
    """Инициализация трех датчиков VL53L0X"""
    try:
        GPIO.setup(SENSOR1_XSHUT, GPIO.OUT)
        GPIO.setup(SENSOR2_XSHUT, GPIO.OUT)
        GPIO.setup(SENSOR3_XSHUT, GPIO.OUT)
        
        # Выключаем все датчики
        GPIO.output(SENSOR1_XSHUT, GPIO.LOW)
        GPIO.output(SENSOR2_XSHUT, GPIO.LOW)
        GPIO.output(SENSOR3_XSHUT, GPIO.LOW)
        time.sleep(0.5)
        
        # Инициализируем датчики с разными адресами
        self.bus = smbus2.SMBus(1)  # Создаем один экземпляр шины I2C
        self.sensors = []  # Очищаем список датчиков
        
        self.init_sensor(SENSOR1_XSHUT, 0x29)
        self.init_sensor(SENSOR2_XSHUT, 0x30)
        self.init_sensor(SENSOR3_XSHUT, 0x31)
        
        print(f"Инициализировано {len(self.sensors)} датчиков")
    except Exception as e:
        print(f"Ошибка при инициализации датчиков: {e}")

def init_sensor(self, xshut_pin, new_address):
    """Инициализация одного датчика"""
    try:
        GPIO.output(xshut_pin, GPIO.HIGH)
        time.sleep(0.1)
        
        # Временный датчик для изменения адреса
        temp_sensor = VL53L0X.VL53L0X(i2c_bus=self.bus)
        temp_sensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)
        temp_sensor.change_address(new_address)
        temp_sensor.stop_ranging()
        
        # Создаем основной датчик с новым адресом
        sensor = VL53L0X.VL53L0X(address=new_address, i2c_bus=self.bus)
        sensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)
        self.sensors.append(sensor)
        
        print(f"Датчик на пине {xshut_pin} инициализирован с адресом 0x{new_address:02X}")
    except Exception as e:
        print(f"Ошибка при инициализации датчика на пине {xshut_pin}: {e}")

def get_distances(self):
    """Получение расстояний от всех датчиков"""
    distances = []
    for sensor in self.sensors:
        try:
            distance = sensor.get_distance()
            distances.append(distance if distance > 0 else None)
        except Exception as e:
            print(f"Ошибка при чтении датчика: {e}")
            distances.append(None)
    return distances