from Queue import LifoQueue
from threading import Thread
from time import sleep


class SonificationManager(object):
    def __init__(self, data_streamer, sonifier, mapping):
        """
        Construct the main manager of the program
        :param data_streamer: list of data streamers
        :param sonifier: sonifier with sonifies the data from the data streamers
        """
        self._data_streamer = data_streamer
        self._mapping = mapping
        self._init_sonifier(sonifier)
        self._parameter_names = self._mapping.keys()
        self._value_queues = dict()
        for parameter in self._parameter_names:
            self._value_queues[parameter] = LifoQueue()

    def _init_sonifier(self, sonifier):
        self._sonifier = sonifier
        self._sonifier.set_channels([instrument[1] for instrument in self._mapping.values()])

    def _sonify_param(self, parameter_channel, parameter_name):
        while True:
            sonic_params = self._value_queues[parameter_name].get()
            # tempo is controlled by the manager
            tempo = sonic_params[0]
            self._sonifier.sonify_values_for_channel(sonic_params[1:], parameter_channel)
            print "Sonified {0}: tempo:{1}, pitch:{2}, volume:{3}, duration:{4}".format(parameter_name, *sonic_params)
            sleep(tempo)

    def _cache_data(self):
        while True:
            values = self._data_streamer.get_data_current_state()
            for parameter, mapping_method in self._mapping.items():
                value = values[parameter]
                mapped_notes = self._data_streamer.get_mapper_for_param(parameter, mapping_method[0]).map(value)
                self._value_queues[parameter].put(mapped_notes)

    def run(self):
        caching_thread = Thread(target=self._cache_data)
        caching_thread.start()
        sonification_threads = list()
        for channel, parameter in enumerate(self._parameter_names):
            sonifying_thread = Thread(target=self._sonify_param, args=[channel, parameter])
            sonifying_thread.start()
            sonification_threads.append(sonifying_thread)
        while True:
            continue
        # initialize GUI with data_streamer.list_properties()
        # initialize GUI with sonifier.list_features(d)