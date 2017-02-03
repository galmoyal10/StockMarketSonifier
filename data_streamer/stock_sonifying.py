from Consts import *
from math import ceil
from math import floor


def price_avg_delta_to_pitch(price, avg_price, discretization_factor):
    """
    sonifying price to pitch in the following logic:
    price -> C + (price - <avg price in the given time>) / <discretization factor>
    for exapmle: a change of 1 dollar will cause (1 / discretization notes)
    """
    return C + int(ceil((price - avg_price) / discretization_factor))


def price_avg_delta_to_tempo(price, avg_price):
    """
    sonifying price to tempo in the following logic:
    price -> 1 + <price - <avg price>> beats in a second
    for example: a change of 1 dollar will cause 2 beats per second
    """
    return min(1, (1 / (1 + max(0, (floor(price - avg_price))))))


def price_avg_delta_to_duration(price, avg_price):
    """
    sonifying price to duration in the following logic:
    price -> 0.15 + <price - avg_price> / 10
    for example: a change of 1 dollar will cause a sound with 0.35 diration
    """
    return min(1, max(0, 0.25 + (floor(price - avg_price) / 10)))


def price_avg_delta_to_amp(price, avg_price):
    """
    sonifying price to volume in the following logic:
    price -> 90 + (<price - avg_price> * 5)
    for example: a change of 1 dollar will cause a volume increase of 5
    note: see pygame.midi - play_note-velocity
    """
    return int(max(MINIMAL_VOLUME, min(MAXIMUM_VOLUME, DEFAULT_VOLUME + (floor(price - avg_price) * 5))))
