from A_movement.A_IMission import A_IMission
from common.tactics.ee1.movement.EE1MovementController import EE1MovementController

class A_EE1(A_IMission):
    def __init__(self):
        super().__init__()
        # EE1 Specific, change movementcontroller to the EE1MovementController
        self.mvmnt_controller = EE1MovementController(self.ros_rate)

    def do_mission(self) -> None:
        self.do_mission_camera_recording_everything()