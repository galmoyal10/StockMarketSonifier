class SonificationManager(object):
    def __init__(self, data_streamer, sonifier):
        """
        Construct the main manager of the program
        :param data_streamer: list of data streamers
        :param sonifier: sonifier with sonifies the data from the data streamers
        """
        self._data_streamer = data_streamer
        self._sonifier = sonifier

    def run(self):
        # initialize GUI with data_streamer.list_properties()
        # initialize GUI with sonifier.list_features()
        pass