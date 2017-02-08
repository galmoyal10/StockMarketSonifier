from midi_wrapper import MidiWrapper
from Consts import SoundParams


class Sonifier(object):
    """
    data sonifier using MIDI
    """
    def __init__(self):
        self._player = MidiWrapper()
        self._supported_sonifiable_params = self.get_supported_sonifiable_params()

    def set_channels(self, instruments):
        """
        initializes channels with given instruments
        see https://www.midi.org/specifications/item/gm-level-1-sound-set for instruments list
        :param instruments:
        :return:
        """
        for channel_index, instument in enumerate(instruments):
            self._player.set_channel_instrument(channel_index, instument)

    def sonify_values_for_channel(self, sonic_params, channel):
        """
        play values for a given channel
        :param sonic_params: sonic params of note
        :param channel: channel to play to note in
        """
        self._player.get_channel(channel).play_note(*sonic_params)

    @staticmethod
    def get_supported_sonifiable_params():
        """
        returns a list of current supported sonic params
        """
        return [SoundParams.pitch, SoundParams.tempo, SoundParams.amplitude, SoundParams.duration]


