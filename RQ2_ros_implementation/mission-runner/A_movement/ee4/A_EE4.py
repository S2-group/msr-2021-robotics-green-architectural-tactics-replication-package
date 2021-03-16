from A_movement.A_IMission import A_IMission
from common.tactics.ee4.camera.EE4CameraSensor import EE4CameraSensor

class A_EE4(A_IMission):
    def __init__(self):
        super().__init__()
        # EE2 Specific, change CameraSensor to the EE2CameraSensor
        self.camera_controller = EE4CameraSensor()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_only_turns()