from tactics.ee2.EE2CameraController import CameraController

class EE2:
    __camera_controller: CameraController

    def __init__(self):
        self.__camera_controller = CameraController()

    def exit(self):
        self.__camera_controller.exit()