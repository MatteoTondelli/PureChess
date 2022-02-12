

class ArduinoBoard:

    def __init__(self):
        self.stored_positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]
        self.from_square = 0
        self.to_square = 0
        self.is_action_started = False
        self.is_action_finished = False

    def find_move(self, board_str):
        # TODO: check for illegal moves...
        actual_positions = [int(pos) for pos in board_str.split(", ")]

        if len(actual_positions) < len(self.stored_positions):
            # Piece removed from the chessboard.
            # The piece who moves must be the first to be taken away from the chessboard.
            if not self.is_action_started:
                # Moving the first piece.
                self.from_square = [x for x in self.stored_positions if x not in actual_positions][0]
                self.stored_positions = actual_positions
                self.is_action_started = True
                self.is_action_finished = False
            else:
                # Capturing.
                self.to_square = [x for x in self.stored_positions if x not in actual_positions][0]
                self.stored_positions = actual_positions

        elif len(actual_positions) > len(self.stored_positions):
            # Piece back on the board.
            self.to_square = [x for x in actual_positions if x not in self.stored_positions][0]
            self.stored_positions = actual_positions
            self.is_action_started = False
            self.is_action_finished = True


########################################################################################################################


if __name__ == '__main__':

    import chess

    board = chess.Board()
    arduino_board = ArduinoBoard()

    with open("ArduinoSimulation.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        arduino_board.find_move(line.replace("\n", ""))
        if arduino_board.is_action_finished:
            new_move = chess.Move(from_square=arduino_board.from_square, to_square=arduino_board.to_square)
            board.push(new_move)
            print(board)
            print("        ")
