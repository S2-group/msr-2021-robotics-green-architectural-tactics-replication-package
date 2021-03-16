import time
import rospy
from typing import List
from itertools import chain
from rospy.timer import Rate
from abc import ABC, abstractmethod
from geometry_msgs.msg import Twist

from common.modules.movement.models.MovementState import MovementState
from common.modules.movement.models.RotationDirection import RotationDirection
from common.modules.movement.controllers.MovementController import MovementController

from common.modules.sensors.odom.controllers.OdomSensor import OdomSensor
from common.modules.sensors.camera.controllers.CameraSensor import CameraSensor

class IMissionController(ABC):
    state:                        MovementState # Needed to account for that various states the robot can be in
    ros_rate:                     Rate
    rotation_interval_in_seconds: int = 20      # Every X seconds, robot rotates a full 360 degrees

    mvmnt_controller:       MovementController  = None # As every mission will have to rotate and thus move the robot
                                                # It is warranted that this controller is instantiated in the
                                                # Abstract parent class of each mission

    odom_controller:        OdomSensor      = None
    camera_controller:      CameraSensor    = None

    minimal_turn_in_degrees:             int = 60   # What turn is minimally allowed (could help too short turns)
    maximal_turn_in_degrees:             int = 140  # What turn is maximally allowed (could help if robot goes back and forth to same spot)

    current_heading:                     float      # Heading to which robot is currently moving
    forward_stopping_distance_threshold: float = 0.5  # At what distance from an object decide to stop
    next_turn_distance_threshold:        float = 1.5  # How much distance must a future turn provide
    robot_forward_viewing_angle:         int = 40   # Needs to be dividable by 2 without fractions as results
    
    mission_duration:                    int = 120  # Mission duration set at 2 minutes = 120 seconds
    last_turn_time = None
    start_time = None

    def __init__(self):
        rospy.init_node("mission_runner")
        self.ros_rate = rospy.Rate(10)
        self.mvmnt_controller = MovementController(self.ros_rate)
        self.odom_controller = OdomSensor()
        self.camera_controller = CameraSensor() # DISABLE FOR SIMULATION
        self.state = MovementState.STARTING

    @abstractmethod
    def do_mission(self) -> None:
        """Perform the specified mission"""
        pass

    def is_object_in_front(self, ranges: List[float]) -> bool:
        # Check forward ranges for distances withing threshold
        # Stop the robot, as it would probably bump into an object otherwise.
        blocked: bool = False
        for distance in self.get_forward_viewing_ranges(ranges):
            if distance <= self.forward_stopping_distance_threshold and \
                distance != 0.0 and distance > 0.3:
                print("[ROBOT STATE] - BLOCKED")
                #print(f"Blocking distance: {distance}")
                #print(f"Ranges: {ranges}")
                blocked = True
                break

        return blocked

    def get_forward_viewing_ranges(self, ranges) -> List[float]:
        # Seperate only the forward viewing angles from ranges
        # And chain them together Left-side: (0:angle/2) Right-side: (359-angle/2:359)
        half_angle = int(self.robot_forward_viewing_angle / 2)
        return list(
            chain(
                ranges[0:half_angle], 
                ranges[359-half_angle:359]
            )
        )

    def is_it_time_for_full_rotation(self) -> bool:
        return time.time() - self.last_turn_time > self.rotation_interval_in_seconds

    def perform_full_rotation(self) -> None:
        self.mvmnt_controller.drive(Twist())    # Stop robot before performing turn.
        self.ros_rate.sleep()                   # Let the command be processed
        self.mvmnt_controller.turn_full_rotation(RotationDirection.CNTR_CLCKWISE)
        self.last_turn_time = time.time()

    def update_current_heading(self):
        roll, pitch, yaw = self.odom_controller.get_odometry_as_tuple()
        self.current_heading = yaw