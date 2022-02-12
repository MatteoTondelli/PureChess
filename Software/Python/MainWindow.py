import sys
import time
import re

import chess
import chess.svg
import chess.pgn

from main import ArduinoBoard
from MIDI import MIDI, MIDIDevice

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

        self.move_interval_sec = 1

        # Add QSvgWidget to the appropriate layout in order to display the initial board state.
        self.svg_widget = QSvgWidget()
        self.svg_widget.setGeometry(100, 100, 500, 500)
        self.Ui.layout_chess_board.addWidget(self.svg_widget)
        self.update_svg_render()

        # Events.
        self.Ui.action_load_game.triggered.connect(self.load_game)
        self.Ui.btn_start_simulation.clicked.connect(self.parse_simulation)

        # Initialization.
        self.find_midi_outputs()

    def find_midi_outputs(self):
        # Create a QComboBox and add it to the menu.
        cb_input_devices = QtWidgets.QComboBox()
        font = QtGui.QFont("Consolas", 9)
        cb_input_devices.setFont(font)
        midi_input_action = QtWidgets.QWidgetAction(self.Ui.menuConfig)
        midi_input_action.setDefaultWidget(cb_input_devices)
        self.Ui.menuConfig.addAction(midi_input_action)
        # Connect MIDI Output selection event.
        cb_input_devices.currentIndexChanged.connect(self.set_midi_output)
        # Add items.
        midi_input_devices = [device.name for device in self.midi.get_available_devices() if device.is_input]
        cb_input_devices.addItems(midi_input_devices)

    def set_midi_output(self, index):
        print("DEBUG:\tSet MIDI Output: {}".format(index))

    def load_game(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Pure Chess - Load Game", "", "PGN Files (*.pgn)")
        if file_name:
            pgn = open(file_name)
            self.game = chess.pgn.read_game(pgn)
            self.chess_board.reset()
            for move in self.game.mainline_moves():
                self.chess_board.push(move)
                self.update_svg_render(last_move=move)
                self.update_pgn_trace()
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

        with open("ArduinoSimulation.txt", "r") as file:
            lines = file.readlines()

        for line in lines:
            self.arduino_board.find_move(line.replace("\n", ""))
            if self.arduino_board.is_action_finished:
                new_move = chess.Move(from_square=self.arduino_board.from_square,
                                      to_square=self.arduino_board.to_square)
                self.chess_board.push(new_move)
                self.game = chess.pgn.Game.from_board(self.chess_board)
                print(self.chess_board)
                print("        ")
                self.update_svg_render(last_move=new_move)
                self.update_pgn_trace()
                time.sleep(self.move_interval_sec)


########################################################################################################################


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
