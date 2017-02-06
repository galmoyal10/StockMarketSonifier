from enum import Enum


class SoundParams(Enum):
    pitch = 1
    amplitude = 2
    duration = 3
    tempo = 4

C = 60

# default tempo is one second
DEFAULT_TEMPO = 1
DEFAULT_PITCH = C
DEFAULT_VOLUME = 90
MINIMAL_VOLUME = 40
MAXIMUM_VOLUME = 127
DEFAULT_DURATION = 0.5

PRICE_STAIRS = 2