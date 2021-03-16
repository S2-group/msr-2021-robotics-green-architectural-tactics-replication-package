import rospy
from rospy import Service
from std_srvs.srv import (Empty, EmptyRequest, EmptyResponse)

class EE3ClientConfigurableSampleRate:
    __hardware_name:        str = None
    __sample_rate_default:  int = 60
    __sample_rate_lowered:  int = 30

    __sample_rate_current:  int = None

    __sample_rate_lowered_service: Service
    __sample_rate_default_service: Service

    __change_event_method = None

    def __init__(self, hardware_name: str, change_event, default_sample_rate: int, lowered_sample_rate: int):     # Sample rate default and Sample rate Lowered, logic here, callback method to notify event
        self.__hardware_name = hardware_name
        self.__sample_rate_default = default_sample_rate
        self.__sample_rate_lowered = lowered_sample_rate

        self.__sample_rate_current = self.__sample_rate_default
        self.__change_event_method = change_event                   # Callback method to notify parent

        self.__sample_rate_lowered_service = rospy.Service(hardware_name + '/sample_rate_lowered', Empty, self.__sample_rate_lowered_clbk)
        self.__sample_rate_default_service = rospy.Service(hardware_name + '/sample_rate_default', Empty, self.__sample_rate_default_clbk)

    def __sample_rate_lowered_clbk(self, msg: EmptyRequest) -> EmptyResponse:
        self.__sample_rate_current = self.__sample_rate_lowered
        self.__change_event_method()
        return EmptyResponse()
        
    def __sample_rate_default_clbk(self, msg: EmptyRequest) -> EmptyResponse:
        self.__sample_rate_current = self.__sample_rate_default
        self.__change_event_method()
        return EmptyResponse()

    def get_current_sample_rate(self) -> int:
        return self.__sample_rate_current