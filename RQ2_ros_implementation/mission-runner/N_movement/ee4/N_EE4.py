from N_movement.N_IMission import N_IMission
from common.tactics.ee4.camera.EE4CameraSensor import EE4CameraSensor

class N_EE4(N_IMission):
    def __init__(self):
        super().__init__()
        self.camera_controller = EE4CameraSensor()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_only_turns()