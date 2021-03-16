import rospy
import time
from rospy import ServiceProxy
from std_srvs.srv import (Empty, EmptyRequest, EmptyResponse)

from common.tactics.ee4.EE4OnDemandComponent import EE4OnDemandComponent

class EE4CameraSensor(EE4OnDemandComponent):
    __start_service_proxy: ServiceProxy
    __stop_service_proxy:  ServiceProxy

    def __init__(self):
        super().__init__('camera')
        self.__start_service_proxy = rospy.ServiceProxy('/camera/start', Empty)
        self.__stop_service_proxy = rospy.ServiceProxy('/camera/stop', Empty)

    def start_recording(self) -> None:
        self.spawn()

        time.sleep(3) # grace period for spawning the node

        while True:
            try:
                self.__start_service_proxy(EmptyRequest())
                break
            except:
                continue

    def stop_recording(self) -> None:
        self.__stop_service_proxy(EmptyRequest())

        time.sleep(1) # grace period for despawning the node

        self.despawn()