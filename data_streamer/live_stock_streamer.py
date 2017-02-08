from data_streamer import SonifiableDataStreamer
from data_streamer import DataFetchingException
from yahoo_finance import Share
from yahoo_finance import YQLResponseMalformedError

import datetime
from sonifier.parameter_mapping.parameter_mappers import *
from stock_sonifying import *
from Consts import DEFAULT_VOLUME

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class SonifiableLiveStockStreamer(SonifiableDataStreamer):
    """
    real time stock data streamer
    """

    SONIFICATION_SUPPORT_MAP = {'Price' : [SoundParams.pitch, SoundParams.tempo, SoundParams.amplitude, SoundParams.duration],
                                'Last trade time' : [SoundParams.amplitude]}


    def refreshable(func):
        """
        refreshes the value before executing the function
        """
        def func_wrapper(self, *args, **kwargs):
            self._share.refresh()
            return func(self, *args, **kwargs)

        return func_wrapper

    def __init__(self, share_symbol_name):
        """
        initializes streamer with the given
        """
        self._share = Share(share_symbol_name)
        if self._share.get_name() is None:
            raise Exception("Could not find share symbol named {0}".format(share_symbol_name))

        self._param_fetching_methods = {'Price': self._share.get_price, 'Last trade time':  self._share.get_trade_datetime}

        # maps a parameter to a sound paramter and its corresponding mapping logic
        self._param_to_sound_param = {'Price': self._init_price_mapping(),
                                      'Last trade time': {SoundParams.amplitude : SONIFYING_PARAMS_TO_MAPPERS[SoundParams.amplitude](self._last_trade_to_amp)}}
        self._last_trade_time = datetime.datetime(datetime.MINYEAR, 1, 1)
        self._price_sum = 0
        self._prices_sampled = 0

    # returns a list of the data parameters
    @staticmethod
    def get_data_params():
        """
        returns a list of the data parameters
        :return: a list of parameters for sonification
        """
        return SonifiableLiveStockStreamer.SONIFICATION_SUPPORT_MAP.keys()

    @staticmethod
    def get_supported_sonic_params_for_param(param):
        """
        returns supported sonic params for given stock parameter
        :param param: stock parameter's name
        :return:
        """
        return SonifiableLiveStockStreamer.SONIFICATION_SUPPORT_MAP[param]


    @refreshable
    def get_value(self, parameter):
        """
        :param parameter: the property to query
        :return: current value of the property
        """
        return self._get_value(parameter)

    @refreshable
    def get_data_current_state(self):
        """
        :return: dictionary of properties with their current value
        """
        try:
            parameters = self._param_fetching_methods.keys()
            return {parameter: self._get_value(parameter) for parameter in parameters}
        except YQLResponseMalformedError:
            raise DataFetchingException

    def _get_value(self, parameter):
        """
        gets a value of a single stock parameter
        :param parameter: paramter's name
        :return:
        """
        assert parameter in self._param_fetching_methods.keys(), "Invalid parameter {0}".format(parameter)
        return self._param_fetching_methods[parameter]()

    def get_mapper_for_param(self, param, sound_param):
        """
        see SonifiableDataStreamer
        """
        return self._param_to_sound_param[param][sound_param]

    def get_supported_mappers_for_param(self, param):
        """
        see SonifiableDataStreamer
        """
        return self._param_to_sound_param[param].keys()

    def _update_price_avg(self, price):
        """
        keeps and updated price average since start of sampling
        :param price: current sampled price
        :return: current average after update
        """
        self._prices_sampled += 1
        self._price_sum += price
        return self._price_sum / self._prices_sampled

    def _init_price_mapping(self):
        """
        initializes price mapping to sonic params
        :return:
        """
        return {SoundParams.pitch: SONIFYING_PARAMS_TO_MAPPERS[SoundParams.pitch](self._price_to_pitch),
                SoundParams.tempo: SONIFYING_PARAMS_TO_MAPPERS[SoundParams.tempo](self._price_to_tempo),
                SoundParams.amplitude: SONIFYING_PARAMS_TO_MAPPERS[SoundParams.amplitude](self._price_to_amp),
                SoundParams.duration: SONIFYING_PARAMS_TO_MAPPERS[SoundParams.duration](self._price_to_duration)}
    """
    price mappers
    """
    def _price_to_pitch(self, price_value):
        return self._map_price(price_value, price_avg_delta_to_pitch)

    def _price_to_tempo(self, price_value):
        return self._map_price(price_value, price_avg_delta_to_tempo)

    def _price_to_amp(self, price_value):
        return self._map_price(price_value, price_avg_delta_to_amp)

    def _price_to_duration(self, price_value):
        return self._map_price(price_value, price_avg_delta_to_duration)

    def _map_price(self, price, mapping_func):
        price = float(price)
        avg = self._update_price_avg(price)
        return mapping_func(price, avg)

    def _last_trade_to_amp(self, last_trade_date_str):
        """
        maps trade time to amplitude
        playing the wanted instrument only when a new trade is detected
        """
        last_trade_date = datetime.datetime.strptime(last_trade_date_str[:19], TIME_FORMAT)
        amp = 0
        if last_trade_date > self._last_trade_time:
            self._last_trade_time = last_trade_date
            amp = DEFAULT_VOLUME
        return amp
