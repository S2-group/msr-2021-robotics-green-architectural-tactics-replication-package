from enum import Enum

class MovementState(Enum):
    STARTING = 1
    STOPPING = 2
    BLOCKED  = 3
    DRIVING  = 4