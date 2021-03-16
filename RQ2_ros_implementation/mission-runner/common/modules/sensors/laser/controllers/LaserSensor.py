import rospy
from rospy.topics import Subscriber
from sensor_msgs.msg import LaserScan
from typing import List

from common.architectural.Singleton import Singleton

class LaserSensor(metaclass=Singleton):
    __scan_sub: Subscriber

    __ranges: List = [0.0] * 360 # Initiate list of size 360 (degrees) with 0.0 (default value)

    def __init__(self):
        self.__scan_sub = rospy.Subscriber('/scan', LaserScan, self.__laser_clbk)

    def __laser_clbk(self, msg: LaserScan):
        self.__ranges = msg.ranges
        # VERBOSE
        #print(self.__ranges[0], self.__ranges[90], self.__ranges[180], self.__ranges[270])

    def get_distances(self) -> List[float]:
        return self.__ranges

    # Returns distances at 90 degrees intervals (front - 0, left - 90, back - 180, right - 270)
    # Returns as tuple.
    def get_distances_at_intervals_90(self) -> (float, float, float, float):
        return (self.__ranges[0], self.__ranges[90], self.__ranges[180], self.__ranges[270])