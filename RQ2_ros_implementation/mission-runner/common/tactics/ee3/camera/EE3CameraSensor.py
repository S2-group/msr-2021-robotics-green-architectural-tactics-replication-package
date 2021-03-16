import rospy
import time
from rospy import ServiceProxy
from std_srvs.srv import (Empty, EmptyRequest, EmptyResponse)

from common.tactics.ee3.EE3ConfigurableSampleRate import EE3ConfigurableSampleRate
from common.tactics.energysavings.EnergySavingsManager import EnergySavingsManager

class EE3CameraSensor(EE3ConfigurableSampleRate):
    __start_service_proxy: ServiceProxy
    __stop_service_proxy:  ServiceProxy

    __energy_savings_manager: EnergySavingsManager

    def __init__(self):
        super().__init__('camera')
        self.__energy_savings_manager = EnergySavingsManager()
        self.__start_service_proxy = rospy.ServiceProxy('/camera/start', Empty)
        self.__stop_service_proxy = rospy.ServiceProxy('/camera/stop', Empty)

    def start_recording(self) -> None:
        # EE3, Responsible for sampling when energy is low.
        if not self.__energy_savings_manager.is_energy_budget_sufficient():
            self.sample_rate_lower()
        else:
            self.sample_rate_default()

        time.sleep(1) # Give grace period
        self.__start_service_proxy(EmptyRequest())

    # EE3 sampling not needed when stopping recording, sampling rate is decided before starting.
    # As it cannot be updated live.
    def stop_recording(self) -> None:
        self.__stop_service_proxy(EmptyRequest())