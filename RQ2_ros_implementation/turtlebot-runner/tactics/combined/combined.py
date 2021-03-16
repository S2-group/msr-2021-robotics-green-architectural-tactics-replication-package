import os
import subprocess as sp

from tactics.ee4.EE4ClientOnDemandComponent import EE4ClientOnDemandComponent

class Combined:
    __dir_path = None
    __camera_ondemand_controller: EE4ClientOnDemandComponent
    __camera_process: sp.Popen

    def __init__(self):
        self.__camera_process = None
        self.__dir_path = os.path.dirname(os.path.realpath(__file__))
        self.__camera_ondemand_controller = EE4ClientOnDemandComponent(component_name='camera', change_event=self.__spawn_change_event)

    def __spawn_change_event(self):
        if not self.__camera_ondemand_controller.is_spawned(): # When despawned in controller, despawn here.
            print("Despawning CameraSensor!")
            #self.__camera_controller.exit() No longer needed as we terminate
            self.__camera_process.terminate()
        else:
            print("Spawning CameraSensor!")
            path = self.__dir_path + '/CombinedCameraController.py'
            self.__camera_process = sp.Popen(['python3', path])

    def exit(self):
        self.__camera_process.terminate()