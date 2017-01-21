from abc import ABCMeta, abstractmethod


class ParameterMapper(object):
    __metaclass__ = ABCMeta

    def __init__(self, default_values, mapping_func):
        self._default_values = default_values
        self._mapping_func = mapping_func

    @abstractmethod
    def map(self, value):
        raise NotImplementedError()


class TempoMapper(ParameterMapper):
    def __init__(self, default_pitch, default_amp, default_duration, mapping_func):
        super(TempoMapper, self).__init__([default_pitch, default_amp, default_duration], mapping_func)

    def map(self, value):
        return self._mapping_func(value), self._default_values[0], self._default_values[1], self._default_values[2],


class PitchMapper(ParameterMapper):
    def __init__(self, default_tempo, default_amp, default_duration, mapping_func):
        super(PitchMapper, self).__init__([default_tempo, default_amp, default_duration], mapping_func)

    def map(self, value):
        return self._default_values[0], self._mapping_func(value), self._default_values[1], self._default_values[2]


class AmpMapper(ParameterMapper):
    def __init__(self, default_tempo, default_pitch, default_duration, mapping_func):
        super(AmpMapper, self).__init__([default_tempo, default_pitch, default_duration], mapping_func)

    def map(self, value):
        return self._default_values[0], self._default_values[1], self._mapping_func(value), self._default_values[2]


class DurationMapper(ParameterMapper):
    def __init__(self, default_tempo, default_pitch, default_amp, mapping_func):
        super(DurationMapper, self).__init__([default_tempo, default_pitch, default_amp], mapping_func)

    def map(self, value):
        return self._default_values[0], self._default_values[1], self._default_values[2], self._mapping_func(value)
