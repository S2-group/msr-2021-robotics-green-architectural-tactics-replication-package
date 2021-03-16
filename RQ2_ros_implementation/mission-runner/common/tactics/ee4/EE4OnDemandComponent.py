import rospy
from rospy import ServiceProxy
from std_srvs.srv import (Empty, EmptyRequest, EmptyResponse)

class EE4OnDemandComponent:
    __component_name: str

    __spawn_service: ServiceProxy
    __despawn_service: ServiceProxy

    def __init__(self, component_name: str):
        self.__component_name = component_name

        self.__spawn_service = rospy.ServiceProxy(component_name + '/spawn', Empty)
        self.__despawn_service = rospy.ServiceProxy(component_name + '/despawn', Empty)

    def spawn(self) -> None:
        self.__spawn_service(EmptyRequest())

    def despawn(self) -> None:
        self.__despawn_service(EmptyRequest())