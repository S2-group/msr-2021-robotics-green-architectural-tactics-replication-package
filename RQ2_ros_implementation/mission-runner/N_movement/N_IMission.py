import time
import math
from abc import ABC, abstractmethod
from common.architectural.IMissionController import IMissionController

class N_IMission(IMissionController, ABC):
    def __init__(self):
        super().__init__()

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
        self.last_turn_time = time.time()
        self.start_time = time.time()
        print("Started!")

        while time.time() - self.start_time < self.mission_duration:
            if self.is_it_time_for_full_rotation():
                if recording_only_turns:
                    self.camera_controller.start_recording()
                    self.perform_full_rotation()
                    self.camera_controller.stop_recording()
                else:
                    self.perform_full_rotation()
            
            self.ros_rate.sleep()