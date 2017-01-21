from data_streamer import SonifiableDataStreamer
from yahoo_finance import Share
from sonifier.parameter_mapping import parameter_mappers
from Consts import SoundParams


class SonifiableStockStreamer(SonifiableDataStreamer):
    """
    example snippet:
        yahoo = StockStreamer("YHOO")
        yahoo.get_value("price")
        yahoo.get_value("last_trade_with_time")
    """
    def refreshable(func):
        """
        refreshs the value before executing the function
        """
        def func_wrapper(self, *args, **kwargs):
            self._share.refresh()
            return func(self, *args, **kwargs)

        return func_wrapper

    def __init__(self, share_name):
        self._share = Share(share_name)
        if self._share.get_name() is None:
            raise Exception("Could not find share named {0}".format(share_name))

        self._param_fetching_methods = {'price': self._share.get_price, 'last_trade_with_time':  self._share.get_last_trade_with_time}

        # maps a parameter to a sound paramter and its corresponding mapping logic
        self._param_to_sound_param = {'price': {SoundParams.pitch : parameter_mappers.PitchMapper(120,1,self._price_to_pitch)},
                                      'last_trade_with_time': {SoundParams.amplitude : parameter_mappers.AmpMapper(60,120, self._last_trade_to_amp)}}

    # returns a list of the data parameters
    @staticmethod
    def get_data_params():
        """

        :return: a list of parameters for sonification
        """
        return ['price','last_trade_with_time']

    @refreshable
    def get_value(self, parameter):
        """

        :param parameter: the property to query
        :return: current value of the property
        """
        return self._get_value(parameter)

    @refreshable
    def get_data_current_state(self, requested_params=None):
        """

        :return: dictionary of properties with their current value
        """
        parameters = self._param_fetching_methods.keys()
        if requested_params is not None:
            parameters = requested_params
        return {parameter: self._get_value(parameter) for parameter in parameters}

    def _get_value(self, parameter):
        assert parameter in self._param_fetching_methods.keys(), "Invalid parameter {0}".format(parameter)
        return self._param_fetching_methods[parameter]()

    def get_mapper_for_param(self, param, sound_param):
        return self._param_to_sound_param[param][sound_param]

    def get_supported_mappers_for_param(self, param):
        return self._param_to_sound_param[param].keys()

    def _price_to_pitch(self, price):
        # TODO: implement price to pitch logic
        return 60

    def _last_trade_to_amp(self, last_trade_date):
        # TODO: implement trade to amp logic
        return 120