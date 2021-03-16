from A_movement.A_IMission import A_IMission
from common.tactics.ee2.camera.EE2CameraSensor import EE2CameraSensor

class A_EE2(A_IMission):
    def __init__(self):
        super().__init__()
        # EE2 Specific, change CameraSensor to the EE2CameraSensor
        self.camera_controller = EE2CameraSensor()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_only_turns()