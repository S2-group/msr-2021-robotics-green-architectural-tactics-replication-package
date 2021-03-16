from F_movement.F_IMission import F_IMission

class F_Baseline(F_IMission):
    def __init__(self):
        super().__init__()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_everything()