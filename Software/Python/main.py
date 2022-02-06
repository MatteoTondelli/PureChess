import chess


class ArduinoBoard:

    def __init__(self):
        self.stored_positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]

    def find_move(self, board_str):
        """
        Moves to detect:
        - Simple move
        - Capture
        - Castling
        - Promotion
        

        :param board_str:
        :return:
        """


        from_square = -1
        to_square = -1

        actual_positions = [int(pos) for pos in board_str.split(", ")]

        # move = list(set(self.stored_positions) ^ set(actual_positions))

        from_square = [x for x in self.stored_positions if x not in actual_positions]
        to_square = [x for x in actual_positions if x not in self.stored_positions]

        self.stored_positions = actual_positions

        if len(from_square) > 0:
            from_square = from_square[0]
        else:
            from_square = 0

        if len(to_square) > 0:
            to_square = to_square[0]
        else:
            to_square = 0

        move = [from_square, to_square]

        return move

        # for stored_pos, actual_pos in zip(self.stored_positions, actual_positions):
        #     if stored_pos != actual_pos:
        #         from_square = stored_pos
        #         to_square = actual_pos
        #
        # return from_square, to_square


########################################################################################################################


if __name__ == '__main__':

    board = chess.Board()
    arduino_board = ArduinoBoard()

    with open("ArduinoSimulation.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        move = arduino_board.find_move(line.replace("\n", ""))
        print(move)

        if len(move) > 0:
            new_move = chess.Move(from_square=move[0], to_square=move[1])
            board.push(new_move)

        print(board)


    # arduino_board = chess.Board()
    # my_move = chess.Move(from_square=chess.E7, to_square=chess.E5)
    #
    # for move in board.move_stack:
    #    print(move.uci())
