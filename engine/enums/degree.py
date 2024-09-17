from enum import Enum

class Degree(Enum):
    VERY_LOW, LOW, BELOW_AVERAGE, NEUTRAL, ABOVE_AVERAGE, HIGH, VERY_HIGH = range(7)