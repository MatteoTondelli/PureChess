import MIDI
import random


class PatchElement:

    def __init__(self, midi_reference, midi_channel):
        self.midi_reference = midi_reference
        self.midi_channel = midi_channel
        # self.midi_reference.init_midi()
        self.pitch = 69
        # All controls are list of square names as strings.
        self.pitch_control = []  # TODO: use set?
        self.lfo_rate_ctlin = 0
        self.lfo_rate = random.randint(0, 20)
        self.lfo_rate_control = []
        self.lfo_vca_ctlin = 1
        self.lfo_vca = 0
        self.lfo_vca_control = []

    def change_pitch(self, change):
        random_value = random.randint(1, 10)
        self.pitch = self.pitch + random_value * change
        print("Random: {}\tChange:{}\tPitch:{}".format(random_value, change, self.pitch))
        self.midi_reference.note_in(self.midi_channel, self.pitch)

    def change_lfo_rate(self, change):
        random_value = random.randint(1, 5)
        self.lfo_rate = self.lfo_rate + random_value * change
        print("Random: {}\tChange:{}\tLFO Rate:{}".format(random_value, change, self.lfo_rate))
        self.midi_reference.control_change(self.lfo_rate_ctlin, self.lfo_rate)

    def change_lfo_vca(self, change):
        random_value = random.randint(1, 10)
        self.lfo_vca = self.lfo_vca + random_value * change
        print("Random: {}\tChange:{}\tLFO VCA:{}".format(random_value, change, self.lfo_vca))
        self.midi_reference.control_change(self.lfo_vca_ctlin, self.lfo_vca)
