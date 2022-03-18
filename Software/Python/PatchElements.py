import MIDI
import random


class PatchElement:

    def __init__(self, midi_reference, midi_channel):
        self.midi_reference = midi_reference
        self.midi_channel = midi_channel
        self.midi_reference.init_midi()
        self.pitch = 69
        self.pitch_control = ["e2"]  # TODO: use set?
        self.lfo_rate = random.randint(0, 20)
        self.lfo_rate_control = [""]
        self.lfo_vca = 0
        self.lfo_vcs_control = [""]

    def change_pitch(self, change):
        random_value = random.randint(1, 10)
        self.pitch = self.pitch + random_value * change
        print("Random: {}\tChange:{}\tPitch:{}".format(random_value, change, self.pitch))
        self.midi_reference.note_in(self.midi_channel, self.pitch)

    def change_lfo_rate(self):
        pass

    def change_lfo_vca(self):
        pass

