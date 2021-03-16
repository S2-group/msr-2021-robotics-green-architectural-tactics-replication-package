import time
import rospy
import picamera
from rospy import Service
from std_srvs.srv import (Empty, EmptyRequest, EmptyResponse)
import threading

from tactics.ee3.EE3ClientConfigurableSampleRate import EE3ClientConfigurableSampleRate

class CameraController(EE3ClientConfigurableSampleRate):
    # Operational variable
    __camera = None

    # Predefined variables
    __is_recording:         bool = False

    __start_recording_service: Service
    __stop_recording_service: Service

    __recording_thread: threading.Thread
    __stop_thread: bool = False

    def __init__(self):
        print("Initializing camera controller!")
        # EE3 Sample tactic specific:
        super().__init__(hardware_name='camera', 
                         change_event=self.__sample_rate_change_event,
                         default_sample_rate=60,
                         lowered_sample_rate=30)

        self.__set_camera_object_with_framerate(self.get_current_sample_rate())

        self.__start_recording_service = rospy.Service('/camera/start', Empty, self.__start_recording)
        self.__stop_recording_service = rospy.Service('/camera/stop', Empty, self.__stop_recording)

        self.__recording_thread = threading.Thread(target=self.__recording_worker_thread)
        self.__recording_thread.start()

    def __set_camera_object_with_framerate(self, new_framerate: int):
        was_recording: bool = self.__is_recording
        if self.__is_recording:
            self.__is_recording = False
            time.sleep(1) # give time to stop

        if self.__camera:
            self.__camera.close()
            time.sleep(0.5) # grace period
            
        self.__camera = picamera.PiCamera(framerate=new_framerate)
        self.__camera.resolution = (1280, 720)
        
        if was_recording:
            self.__start_recording(EmptyRequest())

    def __sample_rate_change_event(self) -> None:
        print(f"Sample rate changed to: {self.get_current_sample_rate()}")
        self.__set_camera_object_with_framerate(self.get_current_sample_rate())

    def __start_recording(self, msg: EmptyRequest) -> EmptyResponse:
        print("Camera recording STARTED!")
        self.__is_recording = True
        return EmptyResponse()

    def __stop_recording(self, msg: EmptyRequest) -> EmptyResponse:
        print("Camera recording STOPPED!")
        self.__is_recording = False
        return EmptyResponse()

    def exit(self):
        self.__stop_recording(EmptyRequest())
        time.sleep(1) # Give time to stop

        self.__stop_thread = True
        self.__recording_thread.join() # Wait for thread to stop and join current process

        self.__camera.close() # Close camera object and release resources
        print("Succesfully stopped thread!")

    def __recording_worker_thread(self):
        thread_recording: bool = False

        def thread_start_recording():
            nonlocal thread_recording
            self.__camera.start_recording('/home/pi/VIDEO_TEST.h264')
            thread_recording = True

        def thread_stop_recording():
            nonlocal thread_recording
            self.__camera.stop_recording()
            thread_recording = False

        while True:                             # Keep thread alive
            while self.__is_recording:          # Record if requested through service
                if not thread_recording:        # If not yet recording (first iteration) start recording
                    thread_start_recording()    # Start recording and prevent second call of start recording
                
                time.sleep(0.5)
            
            if thread_recording:                # Broken out of recording loop, if just recorded, stop recording
                thread_stop_recording()         # Stop recording and prevent second call if not recording again

            if self.__stop_thread:
                print("\tThread ordered to stop!")
                break

            time.sleep(0.5)