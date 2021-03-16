import rospy
from rospy import ServiceProxy
from std_srvs.srv import (Empty, EmptyRequest, EmptyResponse)
from common.tactics.energysavings.EnergySavingsManager import EnergySavingsManager

class EE3ConfigurableSampleRate:
    __hardware_name: str = None

    __sample_rate_lowered_service: ServiceProxy
    __sample_rate_default_service: ServiceProxy

    __energy_savings_manager: EnergySavingsManager

    def __init__(self, hardware_name: str):
        self.__hardware_name = hardware_name
        self.__energy_savings_manager = EnergySavingsManager()

        self.__sample_rate_lowered_service = rospy.ServiceProxy(hardware_name + '/sample_rate_lowered', Empty)
        self.__sample_rate_default_service = rospy.ServiceProxy(hardware_name + '/sample_rate_default', Empty)

    def sample_rate_lower(self) -> None:
        if not self.__energy_savings_manager.is_energy_budget_sufficient():
            self.__sample_rate_lowered_service(EmptyRequest())

    def sample_rate_default(self) -> None:
        if self.__energy_savings_manager.is_energy_budget_sufficient():
            self.__sample_rate_default_service(EmptyRequest())