import sys
import rospy
import signal
from geometry_msgs.msg import Twist

# AUTONOMOUS MOVEMENT 
from A_movement.baseline.A_Baseline import A_Baseline
from A_movement.ee1.A_EE1 import A_EE1
from A_movement.ee2.A_EE2 import A_EE2
from A_movement.ee3.A_EE3 import A_EE3
from A_movement.ee4.A_EE4 import A_EE4
from A_movement.combined.A_Combined import A_Combined

# FIXED MOVEMENT
from F_movement.baseline.F_Baseline import F_Baseline
from F_movement.ee1.F_EE1 import F_EE1
from F_movement.ee2.F_EE2 import F_EE2
from F_movement.ee3.F_EE3 import F_EE3
from F_movement.ee4.F_EE4 import F_EE4
from F_movement.combined.F_Combined import F_Combined

# NO MOVEMENT
from N_movement.baseline.N_Baseline import N_Baseline
from N_movement.ee1.N_EE1 import N_EE1
from N_movement.ee2.N_EE2 import N_EE2
from N_movement.ee3.N_EE3 import N_EE3
from N_movement.ee4.N_EE4 import N_EE4
from N_movement.combined.N_Combined import N_Combined

from common.architectural.IMissionController import IMissionController

# RECORDING
from common.recording.MetricsRecorder import MetricsRecorder

def main():
    metrics_recorder = MetricsRecorder()

    def handler(signum, frame):
        print('Ctrl+Z pressed')
        metrics_recorder.stop_recording()
        exit()

    signal.signal(signal.SIGTSTP, handler)

    # =======================================================
    # SPECIFY MISSION TO EXECUTE HERE                       |
    mission_control: IMissionController = A_Baseline()#          |
    #                                                       |
    #========================================================

    mission_control.do_mission()

    print("Mission completed!")
    print("\a") # Alert with beep that experiment has finished.
    metrics_recorder.stop_recording()
    exit()

if __name__ == "__main__":
    main()