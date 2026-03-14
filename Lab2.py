"""
Цель работы
Закрепить навыки проектирования программного обеспечения с использованием паттернов Factory (фабрика) 
и Builder (строитель). Научиться применять эти паттерны для создания гибких, масштабируемых систем 
на примере эмуляции медицинского оборудования.

Постановка задачи
Необходимо разработать программный модуль, имитирующий систему управления медицинским оборудованием 
в отделении интенсивной терапии. Система должна поддерживать:

Создание различных типов устройств (мониторы пациента, шприцевые насосы, ингаляторы и т. д.) через паттерн Фабрика.
Поэтапную сборку сложных медицинских комплексов (например, реанимационных станций) с помощью паттерна Строитель.
Компоненты системы
Абстрактная фабрика (MedicalDeviceFactory) — определяет интерфейс для создания базовых типов устройств.
Конкретные фабрики — реализуют создание конкретных моделей устройств (например, BasicMonitorFactory, AdvancedVentilatorFactory).
Абстрактный строитель (MedicalKitBuilder) — задаёт шаги сборки медицинского комплекта.
Конкретные строители — реализуют сборку конкретных конфигураций (например, EmergencyKitBuilder, DiagnosticKitBuilder).
Директора (KitDirector) — управляет процессом сборки через абстракцию строителя.
Клиентский код — демонстрирует полиморфное создание устройств и сборку комплектов.
Требования к реализации
Реализовать абстрактную фабрику MedicalDeviceFactory с методами:

create_monitor() — возвращает объект монитора пациента.
create_pump() — возвращает объект шприцевого насоса.
create_ventilator() — возвращает объект аппарата ИВЛ.
Создать конкретные фабрики:

BasicMonitorFactory (создаёт упрощённые мониторы).
HighPrecisionPumpFactory (создаёт насосы с микродозированием).
PortableVentilatorFactory (создаёт портативные аппараты ИВЛ).
Определить интерфейс устройства IMedicalDevice с обязательными свойствами (ID, название, статус) и методом operate().

Реализовать конкретные устройства, наследующие IMedicalDevice:

BasicPatientMonitor (отображает пульс, сатурацию, температуру).
MicroDoseInfusionPump (дозирует лекарства с шагом 0.01 мл).
TransportVentilator (поддерживает дыхание в полевых условиях).
Реализовать абстрактного строителя MedicalKitBuilder с методами:

add_monitor()
add_pump()
add_ventilator()
get_result() — возвращает собранный комплект (MedicalKit).
Создать конкретных строителей:

EmergencyKitBuilder (комплект для реанимации: монитор, насос, аппарат ИВЛ).
DiagnosticKitBuilder (комплект для обследования: монитор, насос).
Реализовать директора KitDirector, который:

принимает экземпляр строителя в конструкторе;
имеет метод build_kit(), последовательно вызывающий шаги сборки.
В клиентском коде (run_medical_system()) продемонстрировать:

полиморфное создание устройств через разные фабрики;
сборку двух различных комплектов через директора и разных строителей;
имитацию работы устройств (вызов operate()).
Соблюдать стандарты оформления кода (PEP-8). Избегать жёсткой привязки к конкретным 
классам — использовать интерфейсы и абстракции.

Критерии оценки
«Удовлетворительно»: реализованы абстрактная фабрика, 2–3 конкретных устройства, базовый строитель. 
Код запускается.
«Хорошо»: полностью реализованы фабрика и строитель, 
продемонстрирована полиморфная работа с устройствами, корректно собраны 2 разных комплекта.
«Отлично»: добавлена обработка ошибок (например, отсутствие компонента в комплекте), 
реализована иерархия устройств с наследованием, подготовлен краткий отчёт (1–2 страницы) 
с объяснением выбора паттернов и их преимуществ.
Примечания
Не используйте глобальные переменные.
Избегайте дублирования кода — используйте наследование и композицию.
Добавьте комментарии к ключевым частям кода, объясняя применение паттернов.
"""

from abc import ABC, abstractmethod
from typing import List

# --- Интерфейс медицинского устройства ---

class IMedicalDevice(ABC):
    """
    Базовый интерфейс для всех медицинских приборов.
    """

    def __init__(self, device_id: str, name: str):
        self.device_id = device_id
        self.name = name
        self.status = "STANDBY"  # STATUS: STANDBY / ACTIVE / ERROR

    @abstractmethod
    def operate(self) -> str:
        """
        Имитация работы устройства (возвращает строку с описанием действия).
        """
        pass

    def activate(self):
        """
        Перевод устройства в активный режим.
        """
        self.status = "ACTIVE"
        print(f"[{self.name} {self.device_id}] Активирован")

    def deactivate(self):
        """
        Деактивация устройства.
        """
        self.status = "STANDBY"
        print(f"[{self.name} {self.device_id}] Деактивирован")


# --- Абстрактная фабрика ---

class MedicalDeviceFactory(ABC):
    """
    Определяет интерфейс для создания устройств.
    Конкретные фабрики будут реализовывать создание конкретных моделей.
    """

    @abstractmethod
    def create_monitor(self) -> IMedicalDevice:
        """Создать монитор пациента."""
        pass

    @abstractmethod
    def create_pump(self) -> IMedicalDevice:
        """Создать шприцевой насос."""
        pass

    @abstractmethod
    def create_ventilator(self) -> IMedicalDevice:
        """Создать аппарат ИВЛ."""
        pass


# --- Конкретные фабрики (заполнить) ---

class BasicMonitorFactory(MedicalDeviceFactory):
    """
    Фабрика для создания упрощённых мониторов пациента.
    """

    def create_monitor(self) -> IMedicalDevice:
        # TODO: Создать и вернуть экземпляр BasicPatientMonitor
        pass

    def create_pump(self) -> IMedicalDevice:
        # TODO: Реализовать (можно возвращать заглушку или NotImplementedError)
        pass

    def create_ventilator(self) -> IMedicalDevice:
        # TODO: Реализовать
        pass


class HighPrecisionPumpFactory(MedicalDeviceFactory):
    """
    Фабрика для создания высокоточных шприцевых насосов.
    """

    def create_monitor(self) -> IMedicalDevice:
        # TODO:
        pass

    def create_pump(self) -> IMedicalDevice:
        # TODO: Создать и вернуть экземпляр MicroDoseInfusionPump
        pass

    def create_ventilator(self) -> IMedicalDevice:
        # TODO:
        pass


# --- Конкретные устройства (заполнить) ---

class BasicPatientMonitor(IMedicalDevice):
    """
    Простой монитор пациента (пульс, сатурация, температура).
    """

    def __init__(self, device_id: str):
        super().__init__(device_id, "Базовый монитор")
        # TODO: Добавить специфические атрибуты (диапазоны измерений и т. п.)

    def operate(self) -> str:
        """
        Имитировать сбор данных: сгенерировать случайные значения.
        Вернуть строку вида: "Пульс: 78 уд/мин, SpO2: 98%, T: 36.8°C".
        """
        # TODO
        return ""


class MicroDoseInfusionPump(IMedicalDevice):
    """
    Шприцевой насос с микродозированием.
    """

    def __init__(self, device_id: str):
        super().__init__(device_id, "Насос с микродозированием")
        # TODO: Специфические параметры (объём, шаг дозирования)

    def operate(self) -> str:
        """
        Имитировать подачу лекарства: вернуть строку вида "Дозировано 0.03 мл препарата X".
        """
        # TODO
        return ""


# --- Паттерн «Строитель» (Builder) ---

class MedicalKit:
    """
    Объект-результат: медицинский комплект.
    Содержит список устройств.
    """

    def __init__(self):
        self.devices: List[IMedicalDevice] = []

    def add_device(self, device: IMedicalDevice):
        self.devices.append(device)

    def display_contents(self):
        print("\nСостав комплекта:")
        for dev in self.devices:
            print(f"- {dev.name} ({dev.device_id})")


class MedicalKitBuilder(ABC):
    """
    Абстрактный строитель: задаёт шаги сборки комплекта.
    """

    def __init__(self):
        self.kit = MedicalKit()

    @abstractmethod
    def add_monitor(self):
        """Добавить монитор в комплект."""
        pass

    @abstractmethod
    def add_pump(self):
        """Добавить насос в комплект."""
        pass

    @abstractmethod
    def add_ventilator(self):
        """Добавить аппарат ИВЛ в комплект."""
        pass

    def get_result(self) -> MedicalKit:
        """Вернуть собранный комплект."""
        return self.kit


class EmergencyKitBuilder(MedicalKitBuilder):
    """
    Строитель для реанимационного комплекта.
    Должен содержать:
    - 1 монитор
    - 1 насос
    - 1 аппарат ИВЛ
    """

    def add_monitor(self):
        # TODO: Создать монитор и добавить в self.kit
        pass

    def add_pump(self):
        # TODO
        pass

    def add_ventilator(self):
        # TODO
        pass


# --- Директор (Director) ---

class KitDirector:
    """
    Управляет процессом сборки через абстракцию строителя.
    """

    def __init__(self, builder: MedicalKitBuilder):
        self.builder = builder

    def build_kit(self):
        """
        Собрать комплект по стандартному алгоритму.
        Вызвать методы строителя в нужном порядке.
        """
        self.builder.add_monitor()
        self.builder.add_pump()
        self.builder.add_ventilator()  # Убрать, если не требуется


# --- Клиентский код (демонстрация) ---

def run_medical_system():
    print("== СИСТЕМА УПРАВЛЕНИЯ МЕДИЦИНСКИМ ОБОРУДОВАНИЕМ v1.0 ==")

    # Пример использования Фабрики
    print("\n--- Создание устройств через фабрики ---")
    monitor_factory = BasicMonitorFactory()
    pump_factory = HighPrecisionPumpFactory()

    device1 = monitor_factory.create_monitor()
    device2 = pump_factory.create_pump()

    device1.activate()
    print(device1.operate())
    device1.deactivate()

    device2.activate()
    print(device2.operate())
    device2.deactivate()

    # Пример использования Строителя
    print("\n--- Сборка реанимационного комплекта ---")
    emergency_builder = EmergencyKitBuilder()
    director = KitDirector(emergency_builder)
    director.build_kit()

    emergency_kit = emergency_builder.get_result()
    emergency_kit.display_contents()

    # TODO: Добавить сборку диагностического комплекта через другой строитель


if __name__ == "__main__":
    run_medical_system()
