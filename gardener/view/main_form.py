from os import path

from qgis.PyQt import uic, QtCore, QtWidgets
from qgis.PyQt.QtWidgets import QWidget


class MainForm(QWidget):
    def __init__(self, manager, parent=None):
        super(MainForm, self).__init__(parent)
        self.uifile = path.join(path.dirname(__file__), "ui/main.ui")
        uic.loadUi(self.uifile, self)
