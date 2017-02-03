import pygame.midi as midi
import threading
import time

DEFAULT_INSTRUMENT = 0
MAX_CHANNEL = 15


class MidiWrapper(object):
    """
    wrapper for communication with midi server
    """
    
    class Channel(object):
        """
        represents a single channel of the midi server
        """
        def __init__(self, player, channel_id, instrument):
            self._player = player
            self._ch_id = channel_id
            self.set_instrument(instrument)

        def set_instrument(self, instrument):
            self._player.set_instrument(instrument, self._ch_id)

        def play_note(self, note, velocity, duration):
            t = threading.Thread(target=self._play_note, args=(note, velocity, duration))
            t.start()

        def _play_note(self, note, velocity, duration):
            self._player.note_on(note, velocity, self._ch_id)
            time.sleep(duration)
            self._player.note_off(note, velocity, self._ch_id)

    def __init__(self):
            midi.init()
            self._player = midi.Output(midi.get_default_output_id())
            self._channels = [MidiWrapper.Channel(self._player, i, DEFAULT_INSTRUMENT) for i in range(0,MAX_CHANNEL)]

    def get_channel(self, channel, instrument=None):
        if instrument is not None:
            self._channels[channel].set_instrument(instrument)
        return self._channels[channel]

    def set_channel_instrument(self, channel, instrument):
        self._channels[channel].set_instrument(instrument)