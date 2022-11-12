import serial
import serial.tools.list_ports
import time
import threading


def get_com_ports():
    """
    Return a list of all available COM ports on the local machine.

    :rtype: list[serial.tools.list_ports_common.ListPortInfo]
    """
    return serial.tools.list_ports.comports()


class Arduino(serial.Serial):
    """
    This class is used to interact with Arduino using the serial interface.
    """
    def __init__(self, com_port: str, baud_rate: int):
        # Public attributes.
        self.square_number = list()
        # Private attributes.
        self._is_listening = False
        # Initialization.
        super().__init__(port=com_port, baudrate=baud_rate, timeout=.1)

    def _listen(self):
        while self._is_listening:
            raw_data = self.readline()
            if raw_data:
                try:
                    data = raw_data.decode("utf-8").replace("\r\n", "")
                    self.square_number = data.split(", ")
                except UnicodeDecodeError:
                    # Ignore garbage.
                    pass
            time.sleep(.5)

    def start_listening(self):
        self._is_listening = True
        listening_thread = threading.Thread(target=self._listen, daemon=True)
        listening_thread.start()

    def stop_listening(self):
        self._is_listening = False

    def __del__(self):
        self.stop_listening()


########################################################################################################################

if __name__ == "__main__":
    com = [port.name for port in get_com_ports()]
    my_arduino = Arduino(com[0], 9600)
    my_arduino.start_listening()

    for i in range(10):
        print(my_arduino.square_number)
        time.sleep(1)

    my_arduino.stop_listening()
