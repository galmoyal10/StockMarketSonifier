import time

class SonificationManager(object):
    def __init__(self, data_streamer, sonifier, mapping, sample_rate):
        """
        Construct the main manager of the program
        :param data_streamer: list of data streamers
        :param sonifier: sonifier with sonifies the data from the data streamers
        """
        self._data_streamer = data_streamer
        self._sonifier = sonifier
        self._mapping = mapping
        self._sample_rate = sample_rate

    def _sonify_next_values(self):
        values = []
        mappers = []
        for param, sound_param in self._mapping.items():
            values.append(self._data_streamer.get_value(param))
            mappers.append(self._data_streamer.get_mapper_for_param(param, sound_param))

        self._sonifier.sonify_values(values, mappers)

    def run(self):
        while True:
            time.sleep(self._sample_rate)
            self._sonify_next_values()
        # initialize GUI with data_streamer.list_properties()
        # initialize GUI with sonifier.list_features(d)