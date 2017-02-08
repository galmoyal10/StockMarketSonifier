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
            """
            sends a MIDI note on command, followed by a note off command
            :param note: the note to play
            :param velocity: volume
            :param duration: the duration of the sound
            :return:
            """
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

    @staticmethod
    def get_instruments():
        return  ['Acoustic Grand Piano',
                 'Bright Acoustic Piano',
                 'Electric Grand Piano',
                 'Honky-tonk Piano',
                 'Electric Piano 1',
                 'Electric Piano 2',
                 'Harpsichord',
                 'Clavi',
                 'Celesta',
                 'Glockenspiel',
                 'Music Box',
                 'Vibraphone',
                 'Marimba',
                 'Xylophone',
                 'Tubular Bells',
                 'Dulcimer',
                 'Drawbar Organ',
                 'Percussive Organ',
                 'Rock Organ',
                 'Church Organ',
                 'Reed Organ',
                 'Accordion',
                 'Harmonica',
                 'Tango Accordion',
                 'Acoustic Guitar (nylo',
                 'Acoustic Guitar (stee',
                 'Electric Guitar (jazz',
                 'Electric Guitar (clea',
                 'Electric Guitar (mute',
                 'Overdriven Guitar',
                 'Distortion Guitar',
                 'Guitar harmonics',
                 'Acoustic Bass',
                 'Electric Bass (finger',
                 'Electric Bass (pick)',
                 'Fretless Bass',
                 'Slap Bass 1',
                 'Slap Bass 2',
                 'Synth Bass 1',
                 'Synth Bass 2',
                 'Violin',
                 'Viola',
                 'Cello',
                 'Contrabass',
                 'Tremolo Strings',
                 'Pizzicato Strings',
                 'Orchestral Harp',
                 'Timpani',
                 'String Ensemble 1',
                 'String Ensemble 2',
                 'SynthStrings 1',
                 'SynthStrings 2',
                 'Choir Aahs',
                 'Voice Oohs',
                 'Synth Voice',
                 'Orchestra Hit',
                 'Trumpet',
                 'Trombone',
                 'Tuba',
                 'Muted Trumpet',
                 'French Horn',
                 'Brass Section',
                 'SynthBrass 1',
                 'SynthBrass 2',
                 'Soprano Sax',
                 'Alto Sax',
                 'Tenor Sax',
                 'Baritone Sax',
                 'Oboe',
                 'English Horn',
                 'Bassoon',
                 'Clarinet',
                 'Piccolo',
                 'Flute',
                 'Recorder',
                 'Pan Flute',
                 'Blown Bottle',
                 'Shakuhachi',
                 'Whistle',
                 'Ocarina',
                 'Lead 1 (square)',
                 'Lead 2 (sawtooth)',
                 'Lead 3 (calliope)',
                 'Lead 4 (chiff)',
                 'Lead 5 (charang)',
                 'Lead 6 (voice)',
                 'Lead 7 (fifths)',
                 'Lead 8 (bass + lead)',
                 'Pad 1 (new age)',
                 'Pad 2 (warm)',
                 'Pad 3 (polysynth)',
                 'Pad 4 (choir)',
                 'Pad 5 (bowed)',
                 'Pad 6 (metallic)',
                 'Pad 7 (halo)',
                 'Pad 8 (sweep)',
                 'FX 1 (rain)',
                 'FX 2 (soundtrack)',
                 'FX 3 (crystal)',
                 'FX 4 (atmosphere)',
                 'FX 5 (brightness)',
                 'FX 6 (goblins)',
                 'FX 7 (echoes)',
                 'FX 8 (sci-fi)',
                 'Sitar',
                 'Banjo',
                 'Shamisen',
                 'Koto',
                 'Kalimba',
                 'Bag pipe',
                 'Fiddle',
                 'Shanai',
                 'Tinkle Bell',
                 'Agogo',
                 'Steel Drums',
                 'Woodblock',
                 'Taiko Drum',
                 'Melodic Tom',
                 'Synth Drum',
                 'Reverse Cymbal',
                 'Guitar Fret Noise',
                 'Breath Noise',
                 'Seashore',
                 'Bird Tweet',
                 'Telephone Ring',
                 'Helicopter',
                 'Applause',
                 'Gunshot']