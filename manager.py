from Queue import LifoQueue
from threading import Thread
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
        self._value_queues = dict()
        self._values_queue = LifoQueue()

    def _sonify_next_values(self):
        values = []
        mappers = []
        for parameter_name, value in self._values_queue.get().items():
            values.append(value)
            mappers.append(self._data_streamer.get_mapper_for_param(parameter_name, self._mapping[parameter_name]))

        self._sonifier._sonify_values(values, mappers)

    def _cache_data(self):
        while True:
            self._values_queue.put(self._data_streamer.get_data_current_state(self._mapping.keys()))

    def run(self):
        t = Thread(target=self._cache_data)
        t.start()
        while True:
            time.sleep(self._sample_rate)
            self._sonify_next_values()
        # initialize GUI with data_streamer.list_properties()
        # initialize GUI with sonifier.list_features(d)