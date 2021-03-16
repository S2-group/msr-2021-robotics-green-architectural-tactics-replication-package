import rospy
import signal
import subprocess

from tactics.combined.combined import Combined
from tactics.baseline.baseline import Baseline
from tactics.ee2.ee2 import EE2
from tactics.ee3.ee3 import EE3
from tactics.ee4.ee4 import EE4

from common.ClientMetricsController import ClientMetricsController

rospy.init_node("turtlebot-runner")

tactic = Baseline()
metrics = ClientMetricsController()

def handler(signum, frame):
    print('Ctrl+Z pressed')
    tactic.exit()
    metrics.exit()
    exit()

signal.signal(signal.SIGTSTP, handler)

print("Initializing bringup")
# roslaunch turtlebot3_bringup turtlebot3_robot.launch
subprocess.Popen(['roslaunch', 'turtlebot3_bringup', 'turtlebot3_robot.launch'])

print("Initializing node!")

while not rospy.is_shutdown():
    rospy.spin()