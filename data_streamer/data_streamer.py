from abc import ABCMeta, abstractmethod


class DataFetchingException(Exception):
    pass


class SonifiableDataStreamer(object):
    """
    interface for sonifiable data stream
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data_params(self):
        """
        returns a list of parameters for sonification
        """
        raise NotImplementedError()

    @abstractmethod
    def get_supported_sonic_params_for_param(self, param):
        """
        returns a list of sonic params that given param can be mapped to
        """
        raise NotImplementedError()

    @abstractmethod
    def get_data_current_state(self):

        """
        returns dictionary of properties with their current value
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
        returns the corresponding mapper of the given stock param to the given sound param
        """
        raise NotImplementedError()

    @abstractmethod
    def get_supported_mappers_for_param(self, param):
        """
        returns a list of supported sonification mappers for given stock parameter
        """
        raise NotImplementedError()