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

    :param com_port: The name of the COM port.
    :type com_port: str
    :param baud_rate: The baud rate for serial communication.
    :type baud_rate: int
    """
    def __init__(self, com_port: str, baud_rate: int = 9600):
        # Public attributes.
        self.square_number = list()
        # Private attributes.
        self._read_delay_ms = 500
        self._is_listening = False
        # Initialization.
        super().__init__(port=com_port, baudrate=baud_rate, timeout=.1)

    def _listen(self):
        """
        Continuously read from the serial input buffer and store data into ``square_number`` class attribute.
        """
        while self._is_listening:
            raw_data = self.readline()
            if raw_data:
                try:
                    data = raw_data.decode("utf-8").replace("\r\n", "")
                    self.square_number = data.split(", ")
                except UnicodeDecodeError:
                    # Ignore garbage.
                    pass
            time.sleep(self._read_delay_ms / 1000)

    def start_listening(self):
        """
        Start a new listening thread (automatically stop the previous one).
        """
        self.stop_listening()
        time.sleep(self._read_delay_ms / 1000 * 2)
        self._is_listening = True
        listening_thread = threading.Thread(target=self._listen, daemon=True)
        listening_thread.start()

    def stop_listening(self):
        """
        Stop the listening thread.
        """
        self._is_listening = False

    def __del__(self):
        self.stop_listening()


########################################################################################################################


if __name__ == "__main__":
    com = [port.name for port in get_com_ports()]
    my_arduino = Arduino(com[0])
    my_arduino.start_listening()

    for i in range(5):
        print(my_arduino.square_number)
        time.sleep(1)

    my_arduino.stop_listening()
