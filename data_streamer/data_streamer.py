from abc import ABCMeta, abstractmethod

class DataStreamer(object):
    __metaclass__ = ABCMeta
    # returns a list of the data properties

    @abstractmethod
    def get_data_properties(self):
        """

        :return: a list of properties for sonification
        """
        raise NotImplementedError()

    @abstractmethod
    def get_data_current_state(self):

        """

        :return: dictionary of properties with their current value
        """
        raise NotImplementedError()

    @abstractmethods
    def get_value(self, property):
        """

        :param property: the property to query
        :return: current value of the property
        """
        raise NotImplementedError()
