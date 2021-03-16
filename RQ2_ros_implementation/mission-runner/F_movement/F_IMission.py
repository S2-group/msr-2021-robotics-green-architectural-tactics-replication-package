import time

from enum import Enum
from typing import List
from abc import ABC, abstractmethod

from geometry_msgs.msg import Twist

from common.modules.movement.models.MovementState import MovementState

from common.architectural.IMissionController import IMissionController
from common.modules.movement.controllers.MovementController import MovementController
from common.modules.movement.models.RotationDirection import RotationDirection
from common.modules.sensors.laser.controllers.LaserSensor import LaserSensor
from common.modules.sensors.odom.controllers.OdomSensor import OdomSensor

class F_IMission(IMissionController, ABC):
    class ObjectType(Enum):
        WALL    = 1
        OBJECT  = 2

    class SweepingDirection(Enum):
        RIGHT = 1
        LEFT  = 2

    # Operation variables
    mvmnt_command: Twist
    ranges: List

    forward_object_distance_threshold: int
    sweeping_direction: SweepingDirection

    # Controllers
    laser_controller: LaserSensor

    # Configurable variables
    sideways_wall_distance_threshold: int  = 0.5
    sweeping_movement_seconds:        int  = 4

    def __init__(self):
        super().__init__() # Needed for general init of abstract class
        self.mvmnt_command = Twist()
        self.forward_object_distance_threshold = self.forward_stopping_distance_threshold + 0.1
        self.sweeping_direction = self.SweepingDirection.RIGHT
        self.laser_controller = LaserSensor()

    @abstractmethod
    def do_mission(self):
        """Perform Fixed Movement Mission"""
        pass

    def do_mission_camera_recording_everything(self) -> None:
        self.camera_controller.start_recording()
        self.do_mission_baseline(recording_only_turns=False)
        self.camera_controller.stop_recording()

    def do_mission_camera_recording_only_turns(self) -> None:
        self.do_mission_baseline(recording_only_turns=True)

    def do_mission_baseline(self, recording_only_turns: bool) -> None:
        self.last_turn_time = time.time()   # Important for knowing when to turn a full rotation again
        self.start_time = time.time()       # Important for ending correctly (after 2 minutes)
        self.state = MovementState.DRIVING
        self.update_current_heading()
        print("Started!")

        roll = pitch = yaw = 0.0

        while time.time() - self.start_time < self.mission_duration:
            self.ranges = self.laser_controller.get_distances()
            roll, pitch, yaw = self.odom_controller.get_odometry_as_tuple()

            if self.state == MovementState.DRIVING:
                print("Driving...")
                self.mvmnt_command.linear.x = self.mvmnt_controller.default_speed
                self.mvmnt_command.angular.z = self.mvmnt_controller.calculate_self_steering_angular_vel(self.current_heading, yaw)

                # VERBOSE
                #print(f"ANG VEL: {self.mvmnt_command.angular.z}")

                if self.is_object_in_front(self.ranges):
                    self.mvmnt_controller.stop()
                    self.state = MovementState.BLOCKED
                
                #self.check_if_time_for_full_rotation_and_ifso_perform()\
                if self.is_it_time_for_full_rotation():
                    self.mvmnt_controller.stop()
                    
                    if recording_only_turns:
                        self.camera_controller.start_recording()
                        self.perform_full_rotation()
                        self.camera_controller.stop_recording()
                    else:
                        self.perform_full_rotation()

            elif self.state == MovementState.BLOCKED:
                object_type = self.is_object_or_wall()
                if object_type == self.ObjectType.OBJECT:
                    print("Object detected...")
                    self.traverse_object()
                    self.update_current_heading()
                else:
                    print("Wall detected...")
                    degrees, direction = self.calculate_turn_for_wall()
                    self.mvmnt_controller.turn_in_degrees(self.current_heading, degrees, direction)

                    self.update_current_heading()

                    self.mvmnt_controller.drive_to_heading_with_speed_for_seconds(self.current_heading, self.mvmnt_controller.default_speed, self.sweeping_movement_seconds)
                    self.mvmnt_controller.turn_in_degrees(self.current_heading, degrees, direction)

                    self.update_current_heading()

                    self.sweeping_direction = self.SweepingDirection.RIGHT \
                        if self.sweeping_direction == self.SweepingDirection.LEFT \
                        else self.SweepingDirection.LEFT

                self.state = MovementState.DRIVING
                self.update_current_heading()

            #VERBOSE
            #print(f"CURRENT HEADING={self.current_heading} || YAW={yaw}")

            self.mvmnt_controller.drive(self.mvmnt_command)
            self.ros_rate.sleep()

        self.mvmnt_controller.stop()

    def is_object_or_wall(self) -> ObjectType:
        object_type: self.ObjectType = self.ObjectType.WALL
        for distance in self.get_forward_viewing_ranges(self.ranges):
            if distance >= self.forward_object_distance_threshold:
                object_type = self.ObjectType.OBJECT
                break
        
        return object_type
    
    def traverse_object(self) -> None:
        best_traverse_direction: RotationDirection = self.calculate_best_object_traverse_direction()
        self.mvmnt_controller.turn_in_degrees(self.current_heading, 90, best_traverse_direction)
        required_angle = 90 if best_traverse_direction.CLCKWISE else 270

        self.update_current_heading()

        while self.ranges[required_angle] <= self.sideways_wall_distance_threshold:
            self.ranges = self.laser_controller.get_distances()
            self.mvmnt_controller.drive_to_heading_with_speed(self.current_heading, 0.2)
            self.ros_rate.sleep()
        
        # Drive a little further to be sure that the object has been passed
        self.mvmnt_controller.drive_to_heading_with_speed_for_seconds(self.current_heading, 0.2, self.mvmnt_controller.default_traverse_time)
        self.mvmnt_controller.stop()

        opposite_rotation = RotationDirection.CNTR_CLCKWISE \
            if best_traverse_direction == RotationDirection.CLCKWISE \
            else RotationDirection.CLCKWISE
        
        # Rotate back to original heading
        self.mvmnt_controller.turn_in_degrees(self.current_heading, 90, opposite_rotation)
            
    def calculate_turn_for_wall(self) -> (int, RotationDirection):
        # Check sweeping direction, if surroundings allow it, drive accordingly.
        if self.sweeping_direction == self.SweepingDirection.RIGHT and \
            self.ranges[270] <= self.sideways_wall_distance_threshold and self.ranges[270] != 0.0:
            print(f"range={self.ranges[270]}")
            print("CHANGE SWEEPING DIRECTION TO AVOID COLLISION TO LEFT")
            self.sweeping_direction = self.SweepingDirection.LEFT
        elif self.sweeping_direction == self.SweepingDirection.LEFT and \
            self.ranges[90] <= self.sideways_wall_distance_threshold and self.ranges[90] != 0.0:
            print(f"range={self.ranges[90]}")
            print("CHANGE SWEEPING DIRECTION TO AVOID COLLISION TO RIGHT")
            self.sweeping_direction = self.SweepingDirection.RIGHT

        direction = RotationDirection.CLCKWISE \
            if self.sweeping_direction == self.SweepingDirection.RIGHT \
            else RotationDirection.CNTR_CLCKWISE

        return (90, direction)

    def calculate_best_object_traverse_direction(self) -> RotationDirection:
        half_angle = int(self.robot_forward_viewing_angle / 2)

        left = self.ranges[0:half_angle]
        right = self.ranges[359-half_angle:359]

        left_total_distance: float = 0.0
        right_total_distance: float = 0.0  

        for i in range(0, half_angle):
            left_total_distance += float(left[i])
            right_total_distance += float(right[i])

        if left_total_distance < right_total_distance and \
            self.ranges[90] >= self.sideways_wall_distance_threshold:
            return RotationDirection.CNTR_CLCKWISE
        else:
            return RotationDirection.CLCKWISE