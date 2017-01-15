from abc import ABCMeta, abstractmethod


class SonifiableDataStreamer(object):
    __metaclass__ = ABCMeta
    # returns a list of the data properties

    @abstractmethod
    def get_data_params(self):
        """

        :return: a list of parameters for sonification
        """
        raise NotImplementedError()

    @abstractmethod
    def get_data_current_state(self):

        """

        :return: dictionary of properties with their current value
        """
        raise NotImplementedError()

    @abstractmethod
    def get_value(self, param):
        """

        :param param: the property to query
        :return: current value of the property
        """
        raise NotImplementedError()

    @abstractmethod
    def get_mapper_for_param(self, param, sound_param):
        """

        :param param: the parameter to query
        :param sound_param: the sound param to map to
        :return: mapping logic for the property
        """
        raise NotImplementedError()

    def get_supported_mappers_for_param(self, param):
        """

        :param param: the parameter to query
        :return: supported mappers for parameter
        """
        raise NotImplementedError()