from tactics.ee3.EE3CameraController import CameraController

class EE3:
    __camera_controller: CameraController

    def __init__(self):
        self.__camera_controller = CameraController()

    def exit(self):
        self.__camera_controller.exit()