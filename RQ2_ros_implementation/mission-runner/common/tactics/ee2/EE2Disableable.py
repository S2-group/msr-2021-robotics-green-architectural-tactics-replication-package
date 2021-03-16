import rospy
from rospy import ServiceProxy
from std_srvs.srv import (Empty, EmptyRequest, EmptyResponse)

class EE2Disableable:
    __hardware_name: str = None
    __is_disabled_service = None

    __enable_service_proxy:  ServiceProxy
    __disable_service_proxy: ServiceProxy

    def __init__(self, hardware_name: str):
        self.__hardware_name = hardware_name

        self.__enable_service_proxy = rospy.ServiceProxy('/' + hardware_name + '/enable', Empty)
        self.__disable_service_proxy = rospy.ServiceProxy('/' + hardware_name+ '/disable', Empty)

    def enable(self) -> None:
        self.__enable_service_proxy(EmptyRequest())

    def disable(self) -> None:
        self.__disable_service_proxy(EmptyRequest())