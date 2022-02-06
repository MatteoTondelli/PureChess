import serial
import time
from chess import SQUARE_NAMES


arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)

while True:
    data = arduino.readline()
    if data:
        square_number = int(data.decode("utf-8").replace("\r\n", ""))
        print(SQUARE_NAMES[square_number])
    time.sleep(.5)
