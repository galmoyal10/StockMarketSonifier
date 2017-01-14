from data_streamer import DataStreamer
from yahoo_finance import Share


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

        self._method_map = {'price': self._share.get_price, 'last_trade_with_time':  self._share.get_last_trade_with_time}

    # returns a list of the data properties
    def get_data_properties(self):
        """

        :return: a list of properties for sonification
        """
        return self._method_map.keys()

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
        return {property: self._get_value(property) for property in self._method_map}

    def _get_value(self, property):
        assert property in self._method_map.keys(), "Invalid property {0}".format(property)
        return self._method_map[property]()