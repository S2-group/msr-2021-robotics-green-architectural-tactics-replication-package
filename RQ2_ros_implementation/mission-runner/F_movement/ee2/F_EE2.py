from F_movement.F_IMission import F_IMission
from common.tactics.ee2.camera.EE2CameraSensor import EE2CameraSensor

class F_EE2(F_IMission):
    def __init__(self):
        super().__init__()
        self.camera_controller = EE2CameraSensor()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_only_turns()