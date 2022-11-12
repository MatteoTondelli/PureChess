# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(541, 438)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 351))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.layout_chess_board = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.layout_chess_board.setContentsMargins(0, 0, 0, 0)
        self.layout_chess_board.setObjectName("layout_chess_board")
        self.btn_start_simulation = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start_simulation.setGeometry(QtCore.QRect(10, 370, 381, 23))
        self.btn_start_simulation.setObjectName("btn_start_simulation")
        self.txt_pgn_trace = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_pgn_trace.setGeometry(QtCore.QRect(400, 30, 131, 191))
        self.txt_pgn_trace.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txt_pgn_trace.setReadOnly(True)
        self.txt_pgn_trace.setObjectName("txt_pgn_trace")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 10, 131, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(400, 240, 131, 21))
        self.label_2.setObjectName("label_2")
        self.txt_midi_out = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_midi_out.setGeometry(QtCore.QRect(400, 260, 131, 101))
        self.txt_midi_out.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txt_midi_out.setReadOnly(True)
        self.txt_midi_out.setObjectName("txt_midi_out")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 541, 20))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuConfig = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.menuConfig.setFont(font)
        self.menuConfig.setObjectName("menuConfig")
        self.menu_com_port = QtWidgets.QMenu(self.menuConfig)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.menu_com_port.setFont(font)
        self.menu_com_port.setObjectName("menu_com_port")
        self.menu_com_name = QtWidgets.QMenu(self.menu_com_port)
        self.menu_com_name.setObjectName("menu_com_name")
        self.menu_com_baud = QtWidgets.QMenu(self.menu_com_port)
        self.menu_com_baud.setObjectName("menu_com_baud")
        self.menu_midi = QtWidgets.QMenu(self.menuConfig)
        self.menu_midi.setObjectName("menu_midi")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionMIDI = QtWidgets.QAction(MainWindow)
        self.actionMIDI.setObjectName("actionMIDI")
        self.action_load_game = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.action_load_game.setFont(font)
        self.action_load_game.setObjectName("action_load_game")
        self.actionBaud = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        self.actionBaud.setFont(font)
        self.actionBaud.setObjectName("actionBaud")
        self.actionName = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        self.actionName.setFont(font)
        self.actionName.setObjectName("actionName")
        self.actionr = QtWidgets.QAction(MainWindow)
        self.actionr.setObjectName("actionr")
        self.actionf = QtWidgets.QAction(MainWindow)
        self.actionf.setObjectName("actionf")
        self.actionttt = QtWidgets.QAction(MainWindow)
        self.actionttt.setObjectName("actionttt")
        self.menuFile.addAction(self.action_load_game)
        self.menu_com_port.addAction(self.menu_com_name.menuAction())
        self.menu_com_port.addAction(self.menu_com_baud.menuAction())
        self.menuConfig.addAction(self.menu_com_port.menuAction())
        self.menuConfig.addAction(self.menu_midi.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConfig.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_start_simulation.setText(_translate("MainWindow", "START Arduino Simulation"))
        self.label.setText(_translate("MainWindow", "PGN Trace"))
        self.label_2.setText(_translate("MainWindow", "MIDI Out"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuConfig.setTitle(_translate("MainWindow", "Config"))
        self.menu_com_port.setTitle(_translate("MainWindow", "COM Port"))
        self.menu_com_name.setTitle(_translate("MainWindow", "Name"))
        self.menu_com_baud.setTitle(_translate("MainWindow", "Baud"))
        self.menu_midi.setTitle(_translate("MainWindow", "MIDI"))
        self.actionMIDI.setText(_translate("MainWindow", "MIDI"))
        self.action_load_game.setText(_translate("MainWindow", "Load Game"))
        self.actionBaud.setText(_translate("MainWindow", "Baud"))
        self.actionName.setText(_translate("MainWindow", "Name"))
        self.actionr.setText(_translate("MainWindow", "r"))
        self.actionf.setText(_translate("MainWindow", "f"))
        self.actionttt.setText(_translate("MainWindow", "ttt"))
