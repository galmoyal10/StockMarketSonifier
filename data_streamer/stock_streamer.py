from data_streamer import SonifiableDataStreamer
from yahoo_finance import Share
from datetime import datetime
from stock_sonifying import *

TIME_FORMAT = "%I:%M%p"


class SonifiableStockStreamer(SonifiableDataStreamer):
    """
    real time stock data streamer
    """

    def refreshable(func):
        """
        refreshes the value before executing the function
        """
        def func_wrapper(self, *args, **kwargs):
            self._share.refresh()
            return func(self, *args, **kwargs)

        return func_wrapper

    def __init__(self, share_name, price_stairs=10):
        self._share = Share(share_name)
        if self._share.get_name() is None:
            raise Exception("Could not find share named {0}".format(share_name))

        self._param_fetching_methods = {'price': self._share.get_price, 'last trade time':  self._share.get_last_trade_with_time}

        # maps a parameter to a sound paramter and its corresponding mapping logic
        self._param_to_sound_param = {'price': {SoundParams.pitch : SONIFYING_PARAMS_TO_MAPPERS[SoundParams.pitch](self._price_to_pitch),
                                                SoundParams.tempo : SONIFYING_PARAMS_TO_MAPPERS[SoundParams.tempo](self._price_to_tempo)},
                                      'last_trade_with_time': {SoundParams.amplitude : SONIFYING_PARAMS_TO_MAPPERS[SoundParams.amplitude](self._last_trade_to_amp)}}
        self._last_trade_time = datetime(datetime.MINYEAR, 1, 1)
        self._price_stairs = price_stairs
        self._price_sum = 0
        self._prices_sampled = 0

    # returns a list of the data parameters
    @staticmethod
    def get_data_params():
        """
        returns a list of the data parameters
        :return: a list of parameters for sonification
        """
        return ['price', 'last trade time']

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
        parameters = self._param_fetching_methods.keys()
        return {parameter: self._get_value(parameter) for parameter in parameters}

    def _get_value(self, parameter):
        assert parameter in self._param_fetching_methods.keys(), "Invalid parameter {0}".format(parameter)
        return self._param_fetching_methods[parameter]()

    def get_mapper_for_param(self, param, sound_param):
        return self._param_to_sound_param[param][sound_param]

    def get_supported_mappers_for_param(self, param):
        return self._param_to_sound_param[param].keys()

    def _update_price_avg(self, price):
        """
        keeps and updated price average since start of sampling
        :param price: current sampled price
        :return: current average after update
        """
        self._prices_sampled += 1
        self._price_sum = + price
        return self._price_sum / self._prices_sampled

    def _price_to_pitch(self, price):
        """
        maps price to pitch
        :param price: current sampled price
        :return: mapping of price against current average to pitch
        """
        avg = self._update_price_avg(price)
        return price_avg_delta_to_pitch(price, avg, self._price_stairs)

    def _price_to_tempo(self, price):
        """
        maps price to tempo
        :param price: current sampled price
        :return: mapping of price against current average to tempo
        """
        avg = self._update_price_avg(price)
        return price_avg_delta_to_tempo(price, avg)

    def _last_trade_to_amp(self, last_trade_date_str):
        """
        maps trade time to amplitude
        playing the wanted instrument only when a new trade is detected
        """
        last_trade_date = datetime.strptime(last_trade_date_str, last_trade_date_str.split(' -')[0])
        amp = 0
        if last_trade_date > self._last_trade_time:
            self._last_trade_time = last_trade_date
            amp = 127
        return amp
