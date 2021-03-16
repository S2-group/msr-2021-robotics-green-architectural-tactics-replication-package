from N_movement.N_IMission import N_IMission
from common.tactics.ee1.movement.EE1MovementController import EE1MovementController

class N_EE1(N_IMission):
    def __init__(self):
        super().__init__()
        self.mvmnt_controller = EE1MovementController(self.ros_rate)

    def do_mission(self) -> None:
        self.do_mission_camera_recording_everything()