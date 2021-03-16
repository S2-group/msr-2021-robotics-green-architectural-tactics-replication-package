from tactics.baseline.BaselineCameraController import CameraController
class Baseline:
    __camera_controller: CameraController

    def __init__(self):
        self.__camera_controller = CameraController()

    def exit(self):
        self.__camera_controller.exit()