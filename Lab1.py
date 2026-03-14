"""
1. Цель работы
Формирование навыков проектирования архитектуры программного обеспечения с использованием механизмов наследования, 
переопределения методов (method overriding) и расширения функциональности базовых классов. 
Изучение принципа подстановки Лисков на примере эмуляции медицинского оборудования.

2. Постановка задачи
Студенту необходимо реализовать программный модуль, имитирующий работу прикроватного монитора пациента. 
Система должна состоять из иерархии классов, описывающих различные типы медицинских датчиков.

Базовый абстрактный класс AbstractSensor должен реализовывать общую логику:

Инициализацию параметров устройства (ID, частота опроса).
Механизм генерации "сырых" данных (эмуляция сигнала).
Логику форматирования выходного пакета данных.
Дочерние классы (HeartRateSensor, SpO2Sensor, TemperatureSensor) должны:

Наследовать функциональность базового класса.
Переопределять методы генерации данных для соответствия физиологическим нормам 
(синусоида для пульса, малые колебания для температуры).
Реализовывать собственную логику анализа критических состояний (Алармы), используя специфические пороговые значения.
3. Требования к реализации
Категорически запрещено дублировать код инициализации атрибутов (port_id, status) в дочерних классах; 
необходимо использовать вызов super().__init__(...).
Обработка исключительных ситуаций (например, обрыв датчика) должна быть предусмотрена в базовом классе, 
но конкретные сообщения об ошибках могут уточняться в наследниках.
Соблюдать стандарты оформления кода PEP-8.
4. Критерии оценки
«Удовлетворительно»: Реализован базовый класс и один наследник, программа запускается без ошибок интерпретатора.
«Хорошо»: Реализована вся иерархия классов, корректно работает механизм super(), симуляция данных правдоподобна.
«Отлично»: Реализована сложная логика тревог (Alarms), присутствует полиморфная обработка 
списка разнородных датчиков в основном цикле программы.
"""

import random
import time
import math
from abc import ABC, abstractmethod
from datetime import datetime

# --- Вспомогательные классы (не требуют модификации) ---

class SensorStatus:
    """Перечисление статусов работы датчика."""
    ACTIVE = "ACTIVE"
    STANDBY = "STANDBY"
    ERROR = "ERROR"

class DataPacket:
    """Структура данных для передачи в систему мониторинга (эмуляция DTO)."""
    def __init__(self, sensor_id: str, timestamp: float, value: float, unit: str, alarm: bool = False):
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.value = value
        self.unit = unit
        self.alarm = alarm

    def __str__(self):
        status = "[!ALARM!]" if self.alarm else "[OK]"
        time_str = datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S')
        return f"{time_str} | {self.sensor_id} | {self.value:.2f} {self.unit} {status}"


# --- Базовый класс (Требует внимания) ---

class AbstractMedicalSensor(ABC):
    """
    Базовый класс для всех медицинских датчиков.
    Включает в себя общую логику подключения к шине данных и базовую структуру.
    """
    
    def __init__(self, serial_number: str, port: int):
        # TODO: Инициализировать общие поля:
        # self._serial_number
        # self._port
        # self._status (по умолчанию STANDBY)
        # self._current_value (для хранения последнего измерения)
        
        # Подсказка: не забудьте про валидацию порта (должен быть > 0)
        pass

    def activate(self) -> None:
        """Перевод сенсора в активный режим."""
        print(f"[{self.__class__.__name__}] Инициализация hardware по порту {self._port}...")
        self._status = SensorStatus.ACTIVE
        self._on_activate_hook()

    def _on_activate_hook(self):
        """
        Хук-метод. Может быть переопределен в наследниках для специфической калибровки.
        В базе — пустой.
        """
        pass

    def read_data(self) -> DataPacket:
        """
        Шаблонный метод (Template Method) чтения данных.
        1. Проверяет статус.
        2. Генерирует 'сырой' сигнал (через полиморфный метод).
        3. Обрабатывает сигнал (через полиморфный метод).
        4. Проверяет на тревоги.
        5. Возвращает упакованный пакет.
        """
        if self._status != SensorStatus.ACTIVE:
            raise RuntimeError(f"Сенсор {self._serial_number} не активен!")

        # Шаг 1: Получение сырого значения (симуляция АЦП)
        raw_val = self._simulate_raw_hardware_signal()
        
        # Шаг 2: Приведение к физическим величинам
        phys_val = self._convert_to_physics(raw_val)
        self._current_value = phys_val

        # Шаг 3: Проверка пороговых значений (Alarm Check)
        is_alarm = self._check_vital_signs(phys_val)

        return DataPacket(
            sensor_id=self._serial_number,
            timestamp=time.time(),
            value=phys_val,
            unit=self.get_unit(),
            alarm=is_alarm
        )

    @abstractmethod
    def get_unit(self) -> str:
        """Метод должен вернуть строковое обозначение единицы измерения."""
        pass

    @abstractmethod
    def _simulate_raw_hardware_signal(self) -> float:
        """
        Эмуляция получения данных с 'железа'. 
        В базовом классе нет реализации, так как природа сигналов разная.
        """
        pass

    def _convert_to_physics(self, raw_value: float) -> float:
        """
        По умолчанию считаем, что raw_value уже в нужных единицах.
        Если датчику нужна калибровка, переопределите этот метод.
        """
        return raw_value

    def _check_vital_signs(self, value: float) -> bool:
        """
        Базовая проверка. Если не переопределено — тревог нет.
        """
        return False


# --- Реализация конкретных датчиков (Задание для студентов) ---

class HeartRateSensor(AbstractMedicalSensor):
    """
    Датчик ЧСС (Пульсометр).
    Норма: 60-100 уд/мин.
    """
    def __init__(self, serial_number: str, port: int):
        # TODO: 1. Вызвать конструктор родителя (Super init)
        # TODO: 2. Установить внутренние пороги тревоги (min_hr=50, max_hr=120)
        pass

    def get_unit(self) -> str:
        return "BPM"

    def _simulate_raw_hardware_signal(self) -> float:
        """
        Симуляция: Генерируем случайное значение в диапазоне 60-90 
        с редкими выборосами (аритмия).
        """
        # TODO: Реализовать генерацию. Можно использовать random.gauss(75, 5)
        # Иногда (с вероятностью 10%) выдавать критическое значение > 130 или < 40
        return 0.0

    def _check_vital_signs(self, value: float) -> bool:
        # TODO: Вернуть True, если value выходит за безопасные пределы
        pass

    def _on_activate_hook(self):
        print(">> Калибровка оптического элемента пульсометра завершена.")


class SpO2Sensor(AbstractMedicalSensor):
    """
    Пульсоксиметр (Сатурация кислорода).
    Норма: 95-100%.
    raw_signal приходит в вольтах (0.0 - 5.0 В), нужно конвертировать в проценты.
    """
    def __init__(self, serial_number: str, port: int):
        # TODO: Инициализация через super()
        pass

    def get_unit(self) -> str:
        return "% SpO2"

    def _simulate_raw_hardware_signal(self) -> float:
        # Симулируем вольтаж. Например, 4.8В соответствует 98%.
        # Допустим, 0В = 0%, 5В = 100%.
        # Сгенерируйте случайное напряжение от 4.5 до 5.0 (норма) или ниже (патология)
        return random.uniform(4.0, 5.0)

    def _convert_to_physics(self, raw_value: float) -> float:
        # TODO: Пересчитать вольты в проценты (линейная зависимость 0-5В -> 0-100%)
        pass

    def _check_vital_signs(self, value: float) -> bool:
        # TODO: Тревога, если сатурация ниже 94%
        pass


class TemperatureSensor(AbstractMedicalSensor):
    """
    Датчик температуры тела (термистор).
    """
    # TODO: Реализовать класс полностью самостоятельно по аналогии.
    # Норма 36.6 +/- 0.5.
    # Критично: > 38.0
    pass


# --- Эмуляция работы монитора (Client Code) ---

def run_hospital_monitor():
    print("=== ЗАПУСК СИСТЕМЫ МОНИТОРИНГА ПАЦИЕНТА (v.2.1) ===")
    
    # Реестр датчиков (полиморфизм в действии — храним AbstractMedicalSensor)
    sensors = []

    try:
        # 1. Сборка конфигурации
        hr_module = HeartRateSensor("HR-001", 1)
        spo2_module = SpO2Sensor("OXY-X10", 2)
        # temp_module = TemperatureSensor("THERM-Z", 3)
        
        sensors.append(hr_module)
        sensors.append(spo2_module)
        # sensors.append(temp_module)

        # 2. Активация оборудования
        print("\n--- Активация датчиков ---")
        for s in sensors:
            s.activate()
        
        print("\n--- Начало мониторинга (Ctrl+C для остановки) ---")
        cycle = 0
        while cycle < 10: # Ограничим 10 циклами для теста
            print(f"\n[Цикл опроса #{cycle}]")
            
            for sensor in sensors:
                # ВНИМАНИЕ: Здесь работает полиморфизм. 
                # Нам не важно, какой конкретно это датчик, метод read_data есть у всех.
                try:
                    packet = sensor.read_data()
                    print(packet)
                    
                    if packet.alarm:
                        print(f">>> ВНИМАНИЕ: ВЫЗОВ МЕДПЕРСОНАЛА! Датчик {packet.sensor_id}")
                        
                except Exception as e:
                    print(f"Ошибка опроса датчика: {e}")
            
            time.sleep(1)
            cycle += 1

    except NotImplementedError:
        print("\n[ОШИБКА]: Не реализованы методы базового класса или наследников.")
        print("Обратитесь к методическим указаниям (раздел 3).")
    except AttributeError as e:
        print(f"\n[КРИТИЧЕСКИЙ СБОЙ]: {e}")
        print("Вероятно, вы забыли вызвать super().__init__() в наследнике.")

if __name__ == "__main__":
    run_hospital_monitor()
