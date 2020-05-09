from os import path

from qgis.PyQt import uic, QtCore, QtWidgets
from qgis.PyQt.QtWidgets import QWidget


class MainForm(QWidget):
    def __init__(self, manager, parent=None):
        super(MainForm, self).__init__(parent)
        self.uifile = path.join(path.dirname(__file__), "ui/main.ui")
        self.manager = manager
        uic.loadUi(self.uifile, self)
        self.paramsButton.clicked.connect(self.open_params_widget)

    def open_params_widget(self):
        self.manager.params_widget.show()
