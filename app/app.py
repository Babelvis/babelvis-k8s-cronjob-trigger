#!/usr/bin/env python3
import sys
from PyQt6 import QtWidgets
from interaction.main import IntUi_MainWindow

class App(QtWidgets.QApplication):
    def __init__(self, argv, mainwindow):
        super(QtWidgets.QApplication, self).__init__(argv)
        self.mainWindow = mainwindow()

    def quit(self, argv):
        super(QtWidgets.QApplication, self).quit(argv)

if __name__ == "__main__":
    app = App(sys.argv, IntUi_MainWindow)
    sys.exit(app.exec())
