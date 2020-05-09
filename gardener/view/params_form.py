from os import path

from qgis.PyQt import uic, QtCore, QtWidgets
from qgis.PyQt.QtWidgets import QWidget


class ParamsForm(QWidget):
    def __init__(self, manager, parent=None):
        super(ParamsForm, self).__init__(parent)
        self.uifile = path.join(path.dirname(__file__), "ui/params.ui")
        uic.loadUi(self.uifile, self)
