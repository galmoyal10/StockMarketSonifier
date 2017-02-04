from midi_wrapper import MidiWrapper
from Consts import SoundParams


class Sonifier(object):
    """

    """
    def __init__(self):
        self._player = MidiWrapper()
        self._supported_sonifiable_params = self.get_supported_sonifiable_params()

    # see https://www.midi.org/specifications/item/gm-level-1-sound-set for instruments list
    def set_channels(self, instruments):
        for channel_index, instument in enumerate(instruments):
            self._player.set_channel_instrument(channel_index, instument)

    def sonify(self, data):
        for channel_index, value in enumerate(data):
            self._sonify_value(channel_index, value)

    def sonify_values_for_channel(self, sonic_params, channel):
        self._player.get_channel(channel).play_note(*sonic_params)

    def _sonify_values(self, values, mappers):
        for channel, value, mapping_func in zip(xrange(0, len(values)), values, mappers):
            self._sonify_value(channel, value, mapping_func)

    @staticmethod
    def get_supported_sonifiable_params():
        return [SoundParams.pitch, SoundParams.tempo, SoundParams.amplitude, SoundParams.duration]


