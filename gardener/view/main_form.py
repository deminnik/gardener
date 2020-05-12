from os import path

from qgis.PyQt import uic, QtCore, QtWidgets
from qgis.PyQt.QtWidgets import QWidget

from gardener.present.main_present import MainPresenter


class MainForm(QWidget):
    def __init__(self, manager, parent=None):
        super(MainForm, self).__init__(parent)
        self.uifile = path.join(path.dirname(__file__), "ui/main.ui")
        self.manager = manager
        self.presenter = MainPresenter(self)
        uic.loadUi(self.uifile, self)
        self.paramsButton.clicked.connect(self.openParamsWidget)
        self.suppressButton.clicked.connect(self.suppressVegetation)

    def suppressVegetation(self):
        self.presenter.suppress_vegetation(self.manager.parameters)

    def suppressFinished(self):
        from qgis.core import QgsMessageLog, Qgis
        QgsMessageLog.logMessage("Suppress finished!!!", "Gardener", level=Qgis.Info)


    def openParamsWidget(self):
        self.manager.params_widget.show()
