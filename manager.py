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
        self._run = True

    def _init_sonifier(self, sonifier):
        """
        initializes the sonifier and its channels
        :param sonifier: the given sonifier
        """
        self._sonifier = sonifier
        self._sonifier.set_channels([instrument[1] for instrument in self._mapping.values()])

    def _sonify_param(self, parameter_channel, parameter_name):
        """
        sonifying a single param
        :param parameter_channel: parameter's channel in the sonifier
        :param parameter_name: the parameter's name
        """
        while self._run:
            param_value, sonic_params = self._value_queues[parameter_name].get()
            # tempo is controlled by the manager
            tempo = sonic_params[0]
            print "Sonifing {0}: \n" \
                  "Value: {1} \n" \
                  "Tempo:{2}, Pitch:{3}, Volume:{4}, Duration:{5}\n************************\n".format(parameter_name, param_value, *sonic_params)
            for i in xrange(0, int(1 / tempo)):
                self._sonifier.sonify_values_for_channel(sonic_params[1:], parameter_channel)
                sleep(tempo)

    def _cache_data(self):
        """
        caches stock data for future sonifications
        """
        while self._run:
            try:
                values = self._data_streamer.get_data_current_state()
                for parameter, mapping_method in self._mapping.items():
                    value = values[parameter]
                    mapped_notes = self._data_streamer.get_mapper_for_param(parameter, mapping_method[0]).map(value)
                    self._value_queues[parameter].put((value,mapped_notes))
            except Exception, e:
                print e.message

    def run(self):
        """
        entry point for manager,
        starts caching and sonifying threads and runs in a loop
        """
        self._run = True
        caching_thread = Thread(target=self._cache_data)
        caching_thread.start()
        sonification_threads = list()
        for channel, parameter in enumerate(self._parameter_names):
            sonifying_thread = Thread(target=self._sonify_param, args=[channel, parameter])
            sonifying_thread.start()
            sonification_threads.append(sonifying_thread)

    def stop(self):
        """
        signals the manager to stop running
        """
        self._run = False
