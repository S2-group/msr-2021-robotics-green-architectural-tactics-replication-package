from common.modules.sensors.battery.controllers.BatterySensor import BatterySensor
from common.architectural.Singleton import Singleton

class EnergySavingsManager(metaclass=Singleton):
    # Threshold chosen at 100 on purpose, therefore manager will always state
    # energy budget is insufficient, allowing the tactics to do their magic.
    __battery_percentage_threshold: int = 100
    __energy_controller: BatterySensor

    def __init__(self):
        self.__battery_percentage_threshold = 20
        self.__energy_controller = BatterySensor()
    
    def is_energy_budget_sufficient(self) -> bool:
        """Returns if the energy budget is sufficient based on the current battery percentage"""
        return (self.__energy_controller.get_percentage() > self.__battery_percentage_threshold)