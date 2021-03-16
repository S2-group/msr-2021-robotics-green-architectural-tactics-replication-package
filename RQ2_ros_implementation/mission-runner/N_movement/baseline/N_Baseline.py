# Architectural import
from N_movement.N_IMission import N_IMission

class N_Baseline(N_IMission):
    def __init__(self):
        super().__init__() # Needed for general init of abstract class

    def do_mission(self) -> None:
        self.do_mission_camera_recording_everything()