from enum import Enum
import random


class Direction(Enum):
    Default = 0
    North = 1
    South = -1
    NorthEast = 2
    SouthWest = -2
    East = 3
    West = -3
    SouthEast = 4
    NorthWest = -4


# Immitates random direction changing of a fish
class DirectionChanger:
    def __init__(self, minValue, maxValue):
        self.max_value = maxValue
        self.min_value = minValue
        self.value = random.randint(minValue, maxValue)

    def resetChanger(self):
        self.value = random.randint(self.min_value, self.max_value)

