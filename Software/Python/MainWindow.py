import sys
import time
import re

# TODO: import SerialCommunication instead...
import serial.tools.list_ports

import chess
import chess.svg
import chess.pgn

# TODO: Can this class be merged with SerialCommunication.Arduino?
from main import ArduinoBoard

from MIDI import MIDI, MIDIDevice
from PatchElements import PatchElement

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer

# UI handling.
from GUI.MainWindow_ui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):

    Ui = Ui_MainWindow()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.Ui.setupUi(self)

        self.game = chess.pgn.Game()
        self.chess_board = chess.Board()
        self.arduino_board = ArduinoBoard()
        self.midi = MIDI()
        self.midi_actual_output_device = None

        self.patch_element_list = []

        self.move_interval_sec = 5

        # Add QSvgWidget to the appropriate layout in order to display the initial board state.
        self.svg_widget = QSvgWidget()
        self.svg_widget.setGeometry(100, 100, 500, 500)
        self.Ui.layout_chess_board.addWidget(self.svg_widget)
        self.update_svg_render()

        # Events.
        self.Ui.action_load_game.triggered.connect(self.load_game)
        self.Ui.btn_start_simulation.clicked.connect(self.parse_simulation)

        # Initialization.
        self.find_com_ports()
        self.find_midi_outputs()

    def find_com_ports(self):
        # Create a QComboBox and add it to the menu.
        cb_com_names = QtWidgets.QComboBox()
        font = QtGui.QFont("Consolas", 9)
        cb_com_names.setFont(font)
        com_port_action = QtWidgets.QWidgetAction(self.Ui.menu_com_name)
        com_port_action.setDefaultWidget(cb_com_names)
        self.Ui.menu_com_name.addAction(com_port_action)
        # Connect COM port selection event.
        cb_com_names.currentIndexChanged.connect(self.set_com_port)
        # Add items.
        ports = [device.name for device in serial.tools.list_ports.comports()]
        cb_com_names.addItems(ports)
        # Create a QComboBox and add it to the menu.
        cb_com_baud_rates = QtWidgets.QComboBox()
        font = QtGui.QFont("Consolas", 9)
        cb_com_baud_rates.setFont(font)
        com_port_action = QtWidgets.QWidgetAction(self.Ui.menu_com_baud)
        com_port_action.setDefaultWidget(cb_com_baud_rates)
        self.Ui.menu_com_baud.addAction(com_port_action)
        # Connect baud rate selection event.
        cb_com_baud_rates.currentIndexChanged.connect(self.set_baud_rate)
        # Add items.
        bauds = ["300", "600", "1200", "2400", "4800", "9600",
                 "14400", "19200", "28800", "31250", "38400", "57600", "115200"]
        cb_com_baud_rates.addItems(bauds)
        cb_com_baud_rates.setCurrentText("9600")

    def set_com_port(self, index):
        pass

    def set_baud_rate(self, index):
        pass

    def find_midi_outputs(self):
        # Create a QComboBox and add it to the menu.
        cb_output_devices = QtWidgets.QComboBox()
        font = QtGui.QFont("Consolas", 9)
        cb_output_devices.setFont(font)
        midi_output_action = QtWidgets.QWidgetAction(self.Ui.menu_midi)
        midi_output_action.setDefaultWidget(cb_output_devices)
        self.Ui.menu_midi.addAction(midi_output_action)
        # Connect MIDI Output selection event.
        cb_output_devices.currentIndexChanged.connect(self.set_midi_output)
        # Add items.
        midi_output_devices = [device.name for device in self.midi.get_available_devices() if device.is_output]
        cb_output_devices.addItems(midi_output_devices)

    def set_midi_output(self, index):
        midi_output_devices = [device for device in self.midi.get_available_devices() if device.is_output]
        self.midi_actual_output_device = midi_output_devices[2]
        print("DEBUG:\tSet MIDI Output: {}".format(index))

    def load_game(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Pure Chess - Load Game", "", "PGN Files (*.pgn)")
        if file_name:
            self.init_patch()

            pgn = open(file_name)
            self.game = chess.pgn.read_game(pgn)
            self.chess_board.reset()
            for move in self.game.mainline_moves():
                self.chess_board.push(move)
                self.update_svg_render(last_move=move)
                self.update_pgn_trace()

                # Extract from_square and to_square from move.
                # from_square = chess.SQUARE_NAMES[move.from_square]
                # to_square = chess.SQUARE_NAMES[move.to_square]
                # Send MIDI command.
                self.process_move_send_midi(move.from_square, move.to_square)

                time.sleep(self.move_interval_sec)

    def update_svg_render(self, last_move=None):
        svg_str = chess.svg.board(self.chess_board, size=350, lastmove=last_move)
        svg_bytes = bytearray(svg_str, encoding='utf-8')
        self.svg_widget.renderer().load(svg_bytes)
        QtWidgets.QApplication.processEvents()

    def update_pgn_trace(self):
        moves_string = str(self.game).split("\n")[-1]
        moves_txt = ""
        for i, move in enumerate(re.split(r"\d[.]{1}", moves_string)):
            if i > 0:
                moves_txt += "{}.{}\n".format(i, move)
        self.Ui.txt_pgn_trace.setPlainText(moves_txt)

    def parse_simulation(self):

        self.chess_board.reset()
        self.arduino_board.__init__()
        self.init_patch()

        with open("ArduinoSimulation.txt", "r") as file:
            lines = file.readlines()

        for line in lines:
            self.arduino_board.find_move(line.replace("\n", ""))
            if self.arduino_board.is_action_finished:
                new_move = chess.Move(from_square=self.arduino_board.from_square,
                                      to_square=self.arduino_board.to_square)
                self.chess_board.push(new_move)
                self.game = chess.pgn.Game.from_board(self.chess_board)
                # print(self.chess_board)
                # print("        ")
                self.update_svg_render(last_move=new_move)
                self.update_pgn_trace()

                # Send MIDI command.
                self.process_move_send_midi(self.arduino_board.from_square, self.arduino_board.to_square)

                # Wait for next move...
                time.sleep(self.move_interval_sec)

    def init_patch(self):
        # Create instances of the patch elements to be used in the game.
        # num_of_patch_elements = 4
        # for i in range(num_of_patch_elements):

        self.midi_actual_output_device.init_midi()

        new_patch_element = PatchElement(self.midi_actual_output_device, 0)
        new_patch_element.pitch_control = ["a2", "b2", "c2", "d2"]
        new_patch_element.lfo_rate_control = ["b1", "d1"]
        new_patch_element.lfo_vca_control = ["a1", "c1"]
        new_patch_element.lfo_rate_ctlin = 0
        new_patch_element.lfo_vca_ctlin = 1
        self.patch_element_list.append(new_patch_element)

        new_patch_element = PatchElement(self.midi_actual_output_device, 1)
        new_patch_element.pitch_control = ["e2", "f2", "g2", "h2"]
        new_patch_element.lfo_rate_control = ["e1", "g1"]
        new_patch_element.lfo_vca_control = ["f1", "h1"]
        new_patch_element.lfo_rate_ctlin = 2
        new_patch_element.lfo_vca_ctlin = 3
        self.patch_element_list.append(new_patch_element)

        new_patch_element = PatchElement(self.midi_actual_output_device, 2)
        new_patch_element.pitch_control = ["a7", "b7", "c7", "d7"]
        new_patch_element.lfo_rate_control = ["b8", "d8"]
        new_patch_element.lfo_vca_control = ["a8", "c8"]
        new_patch_element.lfo_rate_ctlin = 4
        new_patch_element.lfo_vca_ctlin = 5
        self.patch_element_list.append(new_patch_element)

        new_patch_element = PatchElement(self.midi_actual_output_device, 3)
        new_patch_element.pitch_control = ["e7", "f7", "g7", "h7"]
        new_patch_element.lfo_rate_control = ["e8", "g8"]
        new_patch_element.lfo_vca_control = ["f8", "h8"]
        new_patch_element.lfo_rate_ctlin = 6
        new_patch_element.lfo_vca_ctlin = 7
        self.patch_element_list.append(new_patch_element)

    def process_move_send_midi(self, control, new_value):
        # TODO: when a piece is captured, send general trigger to the patch.
        # Find the control.
        square_name = chess.SQUARE_NAMES[control]
        for element in self.patch_element_list:
            # Compute the value change.
            start = int(square_name[1])
            stop = int(chess.SQUARE_NAMES[new_value][1])
            if chess.Color == chess.WHITE:
                change = stop - start
            else:
                change = start - stop
            if square_name in element.pitch_control:
                element.pitch_control.remove(square_name)
                element.pitch_control.append(chess.SQUARE_NAMES[new_value])
                element.change_pitch(change)
            elif square_name in element.lfo_rate_control:
                element.lfo_rate_control.remove(square_name)
                element.lfo_rate_control.append(chess.SQUARE_NAMES[new_value])
                element.change_lfo_rate(change)
            elif square_name in element.lfo_vca_control:
                element.lfo_vca_control.remove(square_name)
                element.lfo_vca_control.append(chess.SQUARE_NAMES[new_value])
                element.change_lfo_vca(change)


########################################################################################################################


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
