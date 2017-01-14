from data_streamer import DataStreamer
from yahoo_finance import Share
from sonifier.parameter_mapping import parameter_mappers
from Consts import SoundParams

class StockStreamer(DataStreamer):
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
        self._param_to_sound_param = {'price': {SoundParams.pitch : parameter_mappers.PitchMapper(120,1,self._price_to_pitch)},
                                      'last_trade_with_time': {SoundParams.amplitude : parameter_mappers.AmpMapper(60,120, self._last_trade_to_amp)}}

    # returns a list of the data properties
    def get_data_params(self):
        """

        :return: a list of properties for sonification
        """
        return self._param_fetching_methods.keys()

    @refreshable
    def get_value(self, property):
        """

        :param property: the property to query
        :return: current value of the property
        """
        return self._get_value(property)

    @refreshable
    def get_data_current_state(self):
        """

        :return: dictionary of properties with their current value
        """
        return {property: self._get_value(property) for property in self._param_fetching_methods}

    def _get_value(self, property):
        assert property in self._param_fetching_methods.keys(), "Invalid property {0}".format(property)
        return self._param_fetching_methods[property]()

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