from enum import Enum


class SoundParams(Enum):
    pitch = 1
    amplitude = 2
    duration = 3
    tempo = 4

C = 60

# default tempo is one second
DEFAULT_TEMPO = 1