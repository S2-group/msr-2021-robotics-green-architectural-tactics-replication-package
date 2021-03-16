from A_movement.A_IMission import A_IMission
from common.tactics.ee3.camera.EE3CameraSensor import EE3CameraSensor

class A_EE3(A_IMission):
    def __init__(self):
        super().__init__()
        # EE2 Specific, change CameraSensor to the EE2CameraSensor
        self.camera_controller = EE3CameraSensor()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_everything()