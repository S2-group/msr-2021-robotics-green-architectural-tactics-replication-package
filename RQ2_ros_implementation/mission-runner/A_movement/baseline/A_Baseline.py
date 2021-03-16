from A_movement.A_IMission import A_IMission

class A_Baseline(A_IMission):
    def __init__(self):
        super().__init__()

    def do_mission(self) -> None:
        self.do_mission_camera_recording_everything()