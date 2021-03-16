import rospy
import time
from rospy import ServiceProxy
from std_srvs.srv import (Empty, EmptyRequest, EmptyResponse)

from common.tactics.ee2.EE2Disableable import EE2Disableable

class EE2CameraSensor(EE2Disableable):
    __start_service_proxy: ServiceProxy
    __stop_service_proxy:  ServiceProxy

    def __init__(self):
        super().__init__('camera')
        self.__start_service_proxy = rospy.ServiceProxy('/camera/start', Empty)
        self.__stop_service_proxy = rospy.ServiceProxy('/camera/stop', Empty)

    def start_recording(self) -> None:
        self.enable()
        time.sleep(1)
        self.__start_service_proxy(EmptyRequest())

    def stop_recording(self) -> None:
        self.__stop_service_proxy(EmptyRequest())
        time.sleep(1)
        self.disable()