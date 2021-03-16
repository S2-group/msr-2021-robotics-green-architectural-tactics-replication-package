from common.modules.sensors.cpu.controllers.CPUSensor import CPUSensor
from common.modules.sensors.ram.controllers.RAMSensor import RAMSensor
from common.modules.sensors.battery.controllers.BatterySensor import BatterySensor
import threading
import time

class MetricsRecorder:
    __cpu_sensor: CPUSensor
    __ram_sensor: RAMSensor
    __bat_sensor: BatterySensor

    __may_threads_exist: bool
    __is_recording: bool
    __recording_thread: threading.Thread

    __metrics_file = None

    def __init__(self):
        self.__cpu_sensor = CPUSensor()
        self.__ram_sensor = RAMSensor()
        self.__bat_sensor = BatterySensor()

        self.__metrics_file = open('mission_runner_metrics.txt', 'w+')

        self.__is_recording = True
        self.__recording_thread = threading.Thread(target=self.__recording)
        self.__recording_thread.start()

    def stop_recording(self):
        print("Stop recording metrics")
        self.__is_recording = False
        time.sleep(1) # grace period
        self.__metrics_file.close()

    def __recording(self):
        while self.__is_recording:
            cpu_usage:      float = self.__cpu_sensor.get_percentage()
            ram_usage:      float = self.__ram_sensor.get_percentage()
            bat_percentage: float = self.__bat_sensor.get_percentage()

            self.__metrics_file.write(str(cpu_usage) + "," + str(ram_usage) + "," + str(bat_percentage) + "\n")
            time.sleep(0.1)
        
        print("Stopped recording thread")