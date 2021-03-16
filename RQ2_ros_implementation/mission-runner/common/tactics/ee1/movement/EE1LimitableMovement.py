import time
from geometry_msgs.msg import Twist
from common.tactics.energysavings.EnergySavingsManager import EnergySavingsManager

class EE1LimitableMovement:
    __energy_savings_manager: EnergySavingsManager
    __limit_straight_line_movement_in_seconds: float = 5.0 # Sleep 5 seconds before rotating, to limit straight-line movement

    ## OLD: No longer needed
    # __percentage_limit: float = 1.0 # Agreed upon change from 0.3 -> 1.0 (keep the same speed)

    def __init__(self):
        self.__energy_savings_manager = EnergySavingsManager()

    def limit_straight_line_movement(self) -> None:
        if not self.__energy_savings_manager.is_energy_budget_sufficient or True:
            time.sleep(self.__limit_straight_line_movement_in_seconds)