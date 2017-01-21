import Consts

from data_streamer.data_streamer import SonifiableDataStreamer
from yahoo_finance import Share
from sonifier.parameter_mapping.parameter_mappers import *
from datetime import datetime
from Consts import SoundParams
from functools import partial
from math import ceil
from math import floor
from math import log10
from copy import deepcopy


class HistoricStockStreamer(SonifiableDataStreamer):
    """
    :param share_name: the name of the share
    :param from_date: the beginning of share stats
    :param to_date: the end of share stats
    :param price_stairs: discretization factor for pitch mapping
    """
    def __init__(self, share_name, from_date, to_date, price_stairs):
        self._share = Share(share_name)
        if self._share.get_name() is None:
            raise Exception("Could not find share named {0}".format(share_name))

        self._params = ['Close', 'High', 'Low', 'Open', 'Volume']
        self._init_history(from_date, to_date)
        self._current_day = 0
        self._num_of_days = (datetime.strptime(to_date, "%Y-%m-%d") - datetime.strptime(from_date, "%Y-%m-%d")).days
        self._init_avgs()
        self._price_stairs = price_stairs
        self._param_to_sound_param = {
            'Close': {SoundParams.pitch: PitchMapper(120, 1, partial(self._price_to_pitch, 'Close'))},
            'High': {SoundParams.pitch: PitchMapper(120, 1, partial(self._price_to_pitch, 'High'))},
            'Low': {SoundParams.pitch: PitchMapper(120, 1, partial(self._price_to_pitch, 'Low'))},
            'Open': {SoundParams.pitch: PitchMapper(120, 1, partial(self._price_to_pitch, 'Open'))},
            'Volume': {SoundParams.pitch: PitchMapper(120, 1, self._volume_to_pitch)}}

    def _init_history(self, from_date, to_date):
        self._historic_data = self._share.get_historical(from_date, to_date)
        unwanted_params = [unwanted_param for unwanted_param in self._historic_data[0].keys() if unwanted_param not in self._params]

        def format_day_data(unwanted_params, day):
            for unwanted_param in unwanted_params:
                day.pop(unwanted_param)
            for parameter, value in day.items():
                day[parameter] = float(value)
            return day

        self._historic_data = map(partial(format_day_data, unwanted_params), self._historic_data)

    def _init_avgs(self):
        self._avgs = dict()
        for param in self._params:
            self._avgs[param] = sum([float(day[param]) for day in self._historic_data]) / self._num_of_days

        self._volume_scale = 10 ** floor(log10(self._avgs['Volume']))

    """
    sonifying price in the following logic:
    price -> C + (price - <avg price in the given time>) / <discretization factor>
    """
    def _price_to_pitch(self, price_param, price_value):
        return Consts.C + int(ceil(((price_value - self._avgs[price_param])+0.0000001) / self._price_stairs))

    """
    sonifying trade volume in the following logic:
    volume -> C + (volume - <avg volume in the given time>) / (10 ^ log_10(avg_volume))
    """
    def _volume_to_pitch(self, volume):
        return Consts.C + int(ceil((volume - self._avgs['Volume']) / self._volume_scale))

    def get_mapper_for_param(self, param, sound_param):
        return self._param_to_sound_param[param][sound_param]

    def get_supported_mappers_for_param(self, param):
        return self._param_to_sound_param[param].keys()

    def get_data_current_state(self, requested_params=None):
        # historic streamer is cyclic
        if self._current_day == self._num_of_days:
            self._current_day = 0
        current_state = deepcopy(self._historic_data[self._current_day])
        # if specific fields requested, return only them
        if requested_params is not None:
            for unwanted_field in [unwanted_field for unwanted_field in self._params if unwanted_field not in requested_params]:
                try:
                    current_state.pop(unwanted_field)
                except KeyError:
                    print(current_state)
        self._current_day += 1
        return current_state

    def get_data_params(self):
        return self._params

    def get_value(self, param):
        return self._historic_data[self._current_day][param]