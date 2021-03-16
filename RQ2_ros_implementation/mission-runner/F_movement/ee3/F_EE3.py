from F_movement.F_IMission import F_IMission
from common.tactics.ee3.camera.EE3CameraSensor import EE3CameraSensor

class F_EE3(F_IMission):
    def __init__(self):
        super().__init__()
        self.camera_controller = EE3CameraSensor()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_everything()