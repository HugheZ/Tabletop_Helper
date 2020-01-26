from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QPlainTextEdit, QApplication, QMainWindow, QDockWidget, QAction, QScrollArea
from PyQt5.QtCore import Qt, pyqtSlot, QSettings, QPoint
from UIComponents.Initiative import *
from UIComponents.Lookup import *
from UIComponents.Form import *
from UIComponents.CentralWindow import *

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = CentralWindow()
    window.show()
    app.exec_()
