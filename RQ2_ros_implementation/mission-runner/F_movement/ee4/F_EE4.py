from F_movement.F_IMission import F_IMission
from common.tactics.ee4.camera.EE4CameraSensor import EE4CameraSensor

class F_EE4(F_IMission):
    def __init__(self):
        super().__init__()
        self.camera_controller = EE4CameraSensor()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_only_turns()