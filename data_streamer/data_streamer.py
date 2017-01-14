from abc import ABCMeta, abstractmethod

class DataStreamer(object):
    __metaclass__ = ABCMeta
    # returns a list of the data properties

    @abstractmethod
    def get_data_properties(self):
        raise NotImplementedError()

    @abstractmethod
    def get_data_current_state(self):
        raise NotImplementedError()

    def get_value(self, property):
        state = self.get_data_current_state()
        return state[property]
