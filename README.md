# Pure Chess
## Overview
An Arduino-based chessboard that can interact with a _PureData_ patch.

## Ideas
Arduino scanning matrix of 8x8 hall effect sensors (or alternatively reed switches) that are activated using tiny magnets below the chess pieces.
The chessboard is not able to recognize each single piece, it can only detect if a certain tile is occupied or not, for this reason a Python script must keep track of all the pieces on the board.

Python way to move a piece on the board:
`Move.from_uci('g1f3')`

Arduino should provide the string `g1f3`, according to the state of the sensors.

- Possibility to "play" famous match, by reading a file containing all the moves.
- Saving live match.

## Useful Links
- [Arduino Schematic and Code editor](https://www.circuito.io/)
- [Python Chess](https://python-chess.readthedocs.io/en/latest/)
- [Pure Data Python integration](http://puredata.info/Members/thomas/py/)
