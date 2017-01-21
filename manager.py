from Queue import LifoQueue
from threading import Thread
from data_streamer.stock_streamer import SonifiableStockStreamer
from sonifier.sonifier import  Sonifier
import time
from Tkinter import *

class SonificationManager(object):

    SONIFICATION_INTRUMENTS = [0, 115, 43]

    def __init__(self, data_streamer, sonifier, mapping, sample_rate = 0.5):
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

    def _do_sonify(self):
        while True:
            time.sleep(manager._sample_rate)
            manager._sonify_next_values()

    @staticmethod
    def _initialize_gui():
        master = Tk(className="Sonification Menu")
        master.resizable(width=False, height=False)
        master.geometry('300x300')

        # TODO: Add a choice between data_streams, and deliver data_params, sonification_features accordingly.
        # TODO: Add implemntation for mapping, and history_stock_streamer.

        # create textbox
        e = Entry(master)
        e.pack()
        e.focus_set()

        #create button
        def callback():
            #TODO : Add input validation
            streamer = SonifiableStockStreamer(e.get())
            sonifier = Sonifier(SonificationManager.SONIFICATION_INTRUMENTS)
            #TODO: Add Yarden's mapping implementation here
            mapping = dict()
            manager = SonificationManager(streamer, sonifier, mapping)

            t = Thread(target=manager._cache_data)
            t.start()
            t2 = Thread(target=manager._do_sonify)
            t2.start()

        b = Button(master, text="Sonify stock!", width=10, command=callback)
        b.pack()

        mainloop()

    @staticmethod
    def run():
        SonificationManager._initialize_gui()

        # initialize GUI with data_streamer.list_properties()
        # initialize GUI with sonifier.list_features(d)