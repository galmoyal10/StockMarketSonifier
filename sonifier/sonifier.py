from midi_wrapper import MidiWrapper
from Consts import SoundParams

class Sonifier(object):
    # see https://www.midi.org/specifications/item/gm-level-1-sound-set for instruments list
    def __init__(self, instruments):
        self._player = MidiWrapper()
        self.set_channels(instruments)
        self._supported_sonifiable_params = [SoundParams.pitch, SoundParams.amplitude, SoundParams.duration]

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

    def get_supported_sonifiable_params(self):
        return self._supported_sonifiable_params


