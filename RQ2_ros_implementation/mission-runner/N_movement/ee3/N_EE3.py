from N_movement.N_IMission import N_IMission
from common.tactics.ee3.camera.EE3CameraSensor import EE3CameraSensor

class N_EE3(N_IMission):
    def __init__(self):
        super().__init__()
        self.camera_controller = EE3CameraSensor()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_everything()