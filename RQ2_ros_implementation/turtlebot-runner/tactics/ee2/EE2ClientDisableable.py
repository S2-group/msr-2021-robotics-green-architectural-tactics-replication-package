import rospy
from rospy import Service
from abc import ABC, abstractmethod
from std_srvs.srv import (Empty, EmptyRequest, EmptyResponse)

class EE2ClientDisableable(ABC):
    __hardware_name: str = None
    __is_disabled = False

    __enable_service: Service
    __disable_service: Service

    __change_event_method = None

    def __init__(self, hardware_name: str, change_event):
        self.__hardware_name = hardware_name
        self.__enable_service = rospy.Service(hardware_name + '/enable', Empty, self.__enable_clbk)
        self.__disable_service = rospy.Service(hardware_name + '/disable', Empty, self.__disable_clbk)

        self.__change_event_method = change_event

    def __enable_clbk(self, msg: EmptyRequest) -> EmptyResponse:
        self.__is_disabled = False
        self.__change_event_method()
        return EmptyResponse()

    def __disable_clbk(self, msg: EmptyRequest) -> EmptyResponse:
        self.__is_disabled = True
        self.__change_event_method()
        return EmptyResponse()

    def is_disabled(self) -> bool:
        return self.__is_disabled