from PyQt6 import QtWidgets
from generated.main import Ui_MainWindow

class IntUi_MainWindow(Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self)
        self.mainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.mainWindow)
        
        self.mainWindow.setFixedSize(self.mainWindow.size())
        self.mainWindow.show()
