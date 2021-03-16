from N_movement.N_IMission import N_IMission
from common.tactics.ee2.camera.EE2CameraSensor import EE2CameraSensor

class N_EE2(N_IMission):
    def __init__(self):
        super().__init__()
        self.camera_controller = EE2CameraSensor()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_only_turns()