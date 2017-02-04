from data_streamer import SonifiableDataStreamer
from yahoo_finance import Share
from sonifier.parameter_mapping.parameter_mappers import *
from stock_sonifying import *
import Consts
from Consts import SoundParams
from functools import partial
from math import ceil
from math import floor
from math import log10
import datetime


class HistoricStockStreamer(SonifiableDataStreamer):
    """
    historic stock data streamer
    :param share_name: the name of the share
    :param from_date: the beginning of share stats
    :param to_date: the end of share stats
    """
    def __init__(self, share_name, from_date, to_date):
        self._share = Share(share_name)
        if self._share.get_name() is None:
            raise Exception("Could not find share named {0}".format(share_name))

        self._param_to_sound_param = {
            'Close': self._init_price_param_mapping('Close'),
            'High': self._init_price_param_mapping('High'),
            'Low': self._init_price_param_mapping('Low'),
            'Open': self._init_price_param_mapping('Open'),
            'Volume': {SoundParams.pitch: PitchMapper(self._volume_to_pitch)}}

        self._params = self._param_to_sound_param.keys()
        self._init_history(from_date, to_date)
        self._current_day = 0
        self._max_day = len(self._historic_data)
        self._init_avgs()

    def _init_price_param_mapping(self, price_param_name):
        """
        generates mapping for price related parameters
        :param price_param_name:
        :return:
        """
        return {SoundParams.pitch: SONIFYING_PARAMS_TO_MAPPERS[SoundParams.pitch](partial(self._price_to_pitch, price_param_name)),
                SoundParams.tempo: SONIFYING_PARAMS_TO_MAPPERS[SoundParams.tempo](partial(self._price_to_tempo, price_param_name)),
                SoundParams.amplitude: SONIFYING_PARAMS_TO_MAPPERS[SoundParams.amplitude](partial(self._price_to_amp, price_param_name)),
                SoundParams.duration: SONIFYING_PARAMS_TO_MAPPERS[SoundParams.duration](partial(self._price_to_duration, price_param_name))}

    def _init_history(self, from_date, to_date):
        """
        fetches historic data of the given date range
        """
        if type(from_date) is datetime.date:
            from_date = from_date.strftime("%Y-%m-%d")
        if type(to_date) is datetime.date:
            to_date = to_date.strftime("%Y-%m-%d")

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
        """
        initializes stock parm averages for sonification functions
        """
        self._avgs = dict()
        for param in self._params:
            self._avgs[param] = sum([float(day[param]) for day in self._historic_data]) / self._max_day

        self._volume_scale = 10 ** floor(log10(self._avgs['Volume']))

    # price related sonifying functions
    def _price_to_pitch(self, price_param, price_value):
        return price_avg_delta_to_pitch(price_value, self._avgs[price_param])

    def _price_to_tempo(self, price_param, price_value):
        return price_avg_delta_to_tempo(price_value, self._avgs[price_param])

    def _price_to_amp(self, price_param, price_value):
        return price_avg_delta_to_amp(price_value, self._avgs[price_param])

    def _price_to_duration(self, price_param, price_value):
        return price_avg_delta_to_duration(price_value, self._avgs[price_param])

    def _volume_to_pitch(self, volume):
        """
        sonifying trade volume in the following logic:
        volume -> C + (volume - <avg volume in the given time>) / (10 ^ log_10(avg_volume))
        """
        return Consts.C + int(ceil((volume - self._avgs['Volume']) / self._volume_scale))

    def get_mapper_for_param(self, param, sound_param):
        return self._param_to_sound_param[param][sound_param]

    def get_supported_mappers_for_param(self, param):
        return self._param_to_sound_param[param].keys()

    def get_data_current_state(self):
        # historic streamer is cyclic
        if self._current_day == self._max_day:
            self._current_day = 0
        current_state = self._historic_data[self._current_day]
        self._current_day += 1
        return current_state

    @staticmethod
    def get_data_params():
        return ['Close', 'High', 'Low', 'Open', 'Volume']

    def get_value(self, param):
        # historic streamer is cyclic
        if self._current_day == self._max_day:
            self._current_day = 0
        current_value = self._historic_data[self._current_day][param]
        self._current_day += 1
        return current_value
