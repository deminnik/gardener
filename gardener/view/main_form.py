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
        self.imageLayerComboBox.currentIndexChanged.connect(self.imageryLayerChoose)
        self.indexLayerComboBox.currentIndexChanged.connect(self.indexLayerChoose)
        self.paramsButton.clicked.connect(self.openParamsWidget)
        self.suppressButton.clicked.connect(self.unveilImage)

    def imageryLayerChoose(self):
        self.presenter.imagery_layer_choose(self.imageLayerComboBox.currentLayer())

    def indexLayerChoose(self):
        self.presenter.index_layer_choose(self.indexLayerComboBox.currentLayer())

    def unveilImage(self):
        self.imageryLayerChoose()
        self.indexLayerChoose()
        self.presenter.unveil_image(self.manager.parameters)

    def unveilingFinished(self):
        from qgis.core import QgsMessageLog, Qgis
        QgsMessageLog.logMessage("Unveiling finished", "Gardener", level=Qgis.Info)


    def openParamsWidget(self):
        self.manager.params_widget.show()
