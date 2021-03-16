import time
import math
import random
from typing import List
from geometry_msgs.msg import Twist
from abc import ABC, abstractmethod

# Architectural import
from common.architectural.IMissionController import IMissionController

# Modules import
from common.modules.sensors.laser.controllers.LaserSensor import LaserSensor
from common.modules.movement.controllers.MovementController import MovementController
from common.modules.movement.models.RotationDirection import RotationDirection
from common.modules.movement.models.MovementState import MovementState

class A_IMission(IMissionController, ABC):
    # Operation variables
    mvmnt_command: Twist
    ranges: List

    # Controllers
    laser_controller: LaserSensor

    def __init__(self):
        super().__init__()                    # Needed for general init of abstract class
        self.mvmnt_command = Twist()          # Instantiate command as empty twist for manipulation
        self.laser_controller = LaserSensor()

    @abstractmethod
    def do_mission(self) -> None:
        """Perform autonomous mission"""

    def do_mission_camera_recording_everything(self) -> None:
        self.camera_controller.start_recording()
        self.do_mission_baseline(recording_only_turns=False)
        self.camera_controller.stop_recording()

    def do_mission_camera_recording_only_turns(self) -> None:
        self.do_mission_baseline(recording_only_turns=True)

    def do_mission_baseline(self, recording_only_turns: bool) -> None:
        self.state = MovementState.DRIVING
        self.last_turn_time = time.time()   # Important and needed for correct rotation execution
        self.start_time = time.time()       # Important and needed for correct mission duration
        print("Started!")

        self.update_current_heading()
        roll = pitch = yaw = 0.0

        while time.time() - self.start_time < self.mission_duration:
            self.ranges = self.laser_controller.get_distances()
            roll, pitch, yaw = self.odom_controller.get_odometry_as_tuple()

            if self.state == MovementState.DRIVING:
                print("Driving...")
                self.mvmnt_command.linear.x = self.mvmnt_controller.default_speed
                self.mvmnt_command.angular.z = self.mvmnt_controller.calculate_self_steering_angular_vel(self.current_heading, yaw)

                if self.is_object_in_front(self.ranges):
                    self.mvmnt_controller.stop()
                    self.state = MovementState.BLOCKED
                
                if self.is_it_time_for_full_rotation():
                    self.mvmnt_controller.stop()
                    if recording_only_turns:
                        self.camera_controller.start_recording()
                        self.perform_full_rotation()
                        self.camera_controller.stop_recording()
                    else:
                        self.perform_full_rotation()

            # When blocked, calculate the best degree for turning out of this blockade
            # Perform the turn, and drive away from the blockade.
            elif self.state == MovementState.BLOCKED:
                self.ranges = self.laser_controller.get_distances()
                degrees, direction = self.calculate_best_turning_degree(self.ranges)
                self.mvmnt_controller.turn_in_degrees(self.current_heading, degrees, direction)
                self.state = MovementState.DRIVING
                self.update_current_heading()

            self.mvmnt_controller.drive(self.mvmnt_command)
            self.ros_rate.sleep()

        print("====Mission completed for duration of 2 minutes!====")
        self.mvmnt_controller.stop()
    
    def calculate_best_turning_degree(self, ranges) -> (int, RotationDirection):
        """Calculates the best turn (defined as the heading where the 
        robot could travel the most amount of distance) and returns said turn
        and the required rotation direction as a tuple (int, direction)"""
        rnd_degree = None
        rnd_distance = 0.0
        rnd_direction = None
        for i in range(self.minimal_turn_in_degrees, self.maximal_turn_in_degrees):
            distance_ccw = ranges[i]       # Measure distance for the turn in degrees i counter-clockwise (left)
            distance_cw = ranges[359 - i]  # Measure distance for the turn in degrees i clockwise (right)

            # Pick the best of the two (greatest distance) and set to 
            # rnd_degree, rnd_distance and rnd_direction to return as best turn
            # REPEAT: look if there is even better turn between min and max turn values.
            if distance_ccw > distance_cw and distance_ccw > rnd_distance:
                rnd_degree = i
                rnd_distance = distance_ccw
                rnd_direction = RotationDirection.CNTR_CLCKWISE
            elif distance_cw > distance_ccw and distance_cw > rnd_distance:
                rnd_degree = i
                rnd_distance = distance_cw
                rnd_direction = RotationDirection.CLCKWISE

        return (rnd_degree, rnd_direction)