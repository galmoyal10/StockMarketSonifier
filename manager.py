class SonificationManager(object):
    def __init__(self, data_streamer, sonifier):
        self._data_streamer = data_streamer
        self._sonifier = sonifier

    def run(self):
        # initialize GUI with data_streamer.list_properties()
        # initialize GUI with sonifier.list_features()
