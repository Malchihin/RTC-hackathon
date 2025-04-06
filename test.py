#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import VL53L0X
import smbus2
from typing import Dict, Optional, Tuple

# Конфигурация пинов XSHUT и адресов для датчиков
SENSOR_CONFIG = {
    1: {"xshut_pin": 4, "address": 0x29, "description": "Левый"},
    2: {"xshut_pin": 5, "address": 0x30, "description": "Центральный"},
    3: {"xshut_pin": 6, "address": 0x31, "description": "Правый"}
}

class VL53L0XManager:
    """Класс для управления несколькими датчиками VL53L0X"""
    
    def __init__(self):
        """Инициализация менеджера датчиков"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.bus = smbus2.SMBus(1)
        self.sensors: Dict[int, VL53L0X.VL53L0X] = {}
        self.initialize_all_sensors()
        
    def _hardware_reset(self):
        """Аппаратный сброс всех датчиков"""
        print("Выполняю аппаратный сброс датчиков...")
        for config in SENSOR_CONFIG.values():
            GPIO.setup(config["xshut_pin"], GPIO.OUT)
            GPIO.output(config["xshut_pin"], GPIO.LOW)
        time.sleep(0.5)
        
    def _initialize_single_sensor(self, sensor_id: int) -> bool:
        """Инициализация одного датчика"""
        config = SENSOR_CONFIG.get(sensor_id)
        if not config:
            raise ValueError(f"Неизвестный ID датчика: {sensor_id}")
            
        try:
            # Активируем датчик
            GPIO.output(config["xshut_pin"], GPIO.HIGH)
            time.sleep(0.1)
            
            # Временный экземпляр для изменения адреса
            with VL53L0X.VL53L0X(i2c_bus=self.bus) as temp_sensor:
                temp_sensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)
                
                if config["address"] != 0x29:
                    temp_sensor.change_address(config["address"])
                    time.sleep(0.1)
                
                temp_sensor.stop_ranging()
            
            # Создаем основной экземпляр
            sensor = VL53L0X.VL53L0X(
                address=config["address"],
                i2c_bus=self.bus
            )
            sensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)
            self.sensors[sensor_id] = sensor
            
            print(f"{config['description']} датчик ({sensor_id}) готов. Адрес: 0x{config['address']:02X}")
            return True
            
        except Exception as e:
            print(f"Ошибка инициализации датчика {sensor_id}: {e}")
            return False
    
    def initialize_all_sensors(self) -> Tuple[bool, int]:
        """Инициализация всех датчиков"""
        self._hardware_reset()
        success_count = 0
        
        for sensor_id in SENSOR_CONFIG:
            if self._initialize_single_sensor(sensor_id):
                success_count += 1
                
        success = success_count == len(SENSOR_CONFIG)
        status = "Все датчики готовы" if success else f"Готово {success_count}/{len(SENSOR_CONFIG)} датчиков"
        print(status)
        return success, success_count
    
    def get_distance(self, sensor_id: int) -> Optional[int]:
        """Получить расстояние с указанного датчика в мм"""
        sensor = self.sensors.get(sensor_id)
        if not sensor:
            return None
            
        try:
            distance = sensor.get_distance()
            return distance if 20 < distance < 2000 else None  # Фильтр значений
        except Exception as e:
            print(f"Ошибка чтения датчика {sensor_id}: {e}")
            return None
    
    def get_all_distances(self) -> Dict[int, Optional[int]]:
        """Получить расстояния со всех датчиков"""
        return {
            sensor_id: self.get_distance(sensor_id)
            for sensor_id in SENSOR_CONFIG
        }
    
    def health_check(self) -> bool:
        """Проверка работоспособности всех датчиков"""
        distances = self.get_all_distances()
        return any(d is not None for d in distances.values())
    
    def restart_sensor(self, sensor_id: int) -> bool:
        """Перезапуск конкретного датчика"""
        config = SENSOR_CONFIG.get(sensor_id)
        if not config:
            return False
            
        print(f"Перезапуск датчика {sensor_id}...")
        try:
            # Выключаем датчик
            GPIO.output(config["xshut_pin"], GPIO.LOW)
            time.sleep(0.1)
            
            # Включаем и инициализируем заново
            return self._initialize_single_sensor(sensor_id)
        except Exception as e:
            print(f"Ошибка перезапуска датчика {sensor_id}: {e}")
            return False
    
    def cleanup(self):
        """Корректное завершение работы"""
        print("Завершение работы...")
        for sensor in self.sensors.values():
            try:
                sensor.stop_ranging()
            except:
                pass
        self.bus.close()
        GPIO.cleanup()

def main():
    """Основная функция работы с датчиками"""
    print("Инициализация системы датчиков VL53L0X")
    manager = VL53L0XManager()
    
    try:
        while True:
            distances = manager.get_all_distances()
            print("\n" + "-"*40)
            for sensor_id, dist in distances.items():
                desc = SENSOR_CONFIG[sensor_id]["description"]
                print(f"{desc} датчик: {dist or '--'} мм")
            
            # Проверка работоспособности
            if not manager.health_check():
                print("\nВнимание: не работают все датчики!")
                print("Пытаюсь восстановить соединение...")
                manager.initialize_all_sensors()
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nЗавершение работы по команде пользователя")
    finally:
        manager.cleanup()

if __name__ == "__main__":
    main()
