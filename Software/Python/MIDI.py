import time

import pygame.midi


class MIDIDevice:
    """
    This class describes a general MIDI device.
    """
    def __init__(self):
        self.index = 0
        self.interface = ""
        self.name = ""
        self.is_open = False
        self.is_input = False
        self.is_output = False

        self.midi_out = None

    def __str__(self):
        plain_string = ""
        for key in self.__dict__.keys():
            plain_string += "{}: {}\t".format(key, self.__dict__[key])
        return plain_string

    def init_midi(self):
        self.midi_out = pygame.midi.Output(self.index)

    def write(self):
        self.midi_out.write([[[144, 70], 0]])
        self.midi_out.write([[[0x91, 0x45], 0]])

    def note_in(self, channel, value):
        midi_command = 0x90 + channel
        self.midi_out.write([[[midi_command, value], 0]])

    def control_change(self, channel, value):
        midi_command = 0xB0
        self.midi_out.write([[[midi_command, channel, value], 0]])


class MIDI:
    """
    This class is used to interact with MIDI devices on the local PC.
    """
    def __init__(self):
        # Public attributes.
        self.device_list = []
        # Initialization.
        pygame.midi.init()

    def __del__(self):
        pygame.midi.quit()

    def get_available_devices(self):
        self.device_list.clear()
        for device_index in range(pygame.midi.get_count()):
            device_info = pygame.midi.get_device_info(device_index)
            if device_info is not None:
                device = MIDIDevice()
                device.index = device_index
                device.interface = device_info[0].decode("utf-8")
                device.name = device_info[1].decode("utf-8")
                device.is_input = device_info[2]
                device.is_output = device_info[3]
                device.is_open = device_info[4]
                self.device_list.append(device)
        return self.device_list


########################################################################################################################


if __name__ == "__main__":
    my_midi = MIDI()
    devices = my_midi.get_available_devices()
    # for midi_device in devices:
    #     print(midi_device)
    #     if midi_device.is_output:
    #         try:
    #             midi_device.write()
    #         except:
    #             pass
    my_device = devices[10]
    my_device.midi_out = pygame.midi.Output(my_device.index)
    # my_device.write()
    # my_device.write()
    my_device.control_change(1, 24)
