from A_movement.A_IMission import A_IMission
from common.tactics.ee1.movement.EE1MovementController import EE1MovementController
from common.tactics.combined.camera.CombinedCameraSensor import CombinedCameraSensor

class A_Combined(A_IMission):
    def __init__(self):
        super().__init__()
        # EE1 Specific, change movementcontroller to the EE1MovementController
        self.mvmnt_controller = EE1MovementController(self.ros_rate)    # EE1
        self.camera_controller = CombinedCameraSensor()                 # EE3 and EE4 (EE2 is encapsulated in EE4)

        # With these settings, this mission will be testing all 4 tactics at once (COMBINED)

    def do_mission(self) -> None:
        self.do_mission_camera_recording_only_turns()