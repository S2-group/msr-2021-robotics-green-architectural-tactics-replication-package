import rospy
import time
from rospy import ServiceProxy
from std_srvs.srv import (Empty, EmptyRequest, EmptyResponse)

from common.tactics.ee3.EE3ConfigurableSampleRate import EE3ConfigurableSampleRate
from common.tactics.ee4.EE4OnDemandComponent import EE4OnDemandComponent

from common.tactics.energysavings.EnergySavingsManager import EnergySavingsManager

class CombinedCameraSensor(EE3ConfigurableSampleRate, EE4OnDemandComponent):
    __start_service_proxy: ServiceProxy
    __stop_service_proxy:  ServiceProxy

    __energy_savings_manager: EnergySavingsManager

    def __init__(self):
        EE3ConfigurableSampleRate.__init__(self, hardware_name='camera')
        EE4OnDemandComponent.__init__(self, component_name='camera')

        self.__energy_savings_manager = EnergySavingsManager()

        self.__start_service_proxy = rospy.ServiceProxy('/camera/start', Empty)
        self.__stop_service_proxy = rospy.ServiceProxy('/camera/stop', Empty)

    def start_recording(self) -> None:
        self.spawn() # EE4

        time.sleep(3)

        while True:
            try:
                # EE3, Responsible for sampling when energy is low.
                if not self.__energy_savings_manager.is_energy_budget_sufficient():
                    self.sample_rate_lower()
                else:
                    self.sample_rate_default()

                break
            except:
                continue

        time.sleep(1) # grace period

        self.__start_service_proxy(EmptyRequest())

    def stop_recording(self) -> None:
        self.__stop_service_proxy(EmptyRequest())

        time.sleep(1) # grace period

        self.despawn() # EE4