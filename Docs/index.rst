Welcome to PureChess's documentation!
=====================================

An Arduino-based chessboard that can interact with a PureData patch.

Follow the :doc:`getting_started` guide to dive into.

How It Works?
-------------

A Python application keeps track of the position of all pieces during a chess match and, based on a certain algorithm, sends MIDI mesages to a running 
PureData patch.

The algorithm can be adjusted by the user editing a YAML file.

.. toctree::
   :maxdepth: 2
   :caption: Tutorial:
   :hidden:
   
   getting_started

.. toctree::
   :maxdepth: 2
   :caption: How to Build:
   :hidden:
   
   how_to_build
   chessboard
   sensor_board
   master_board

.. toctree::
   :maxdepth: 2
   :caption: Developers:
   :hidden:
   
   arduino_code
   python_application
   pure_data
