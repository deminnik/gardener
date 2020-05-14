from os import path
from functools import partial

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget, QFileDialog
from qgis.core import Qgis
from qgis.core import QgsProject

from gardener.present.main_present import MainPresenter
from gardener.present.params_present import ParamsPresenter


class Form(QWidget):
    def __init__(self, uifile, presenter, manager, parent=None):
        super().__init__(parent)
        uipath = "ui"
        ui = path.join(path.dirname(__file__), f"{uipath}/{uifile}")
        uic.loadUi(ui, self)
        self.manager = manager
        self.presenter = presenter(self)
        self.messageBar = self.manager.iface.messageBar()

    def pushSuccessMessage(self, message):
        self.messageBar.pushMessage("Success", message, level=Qgis.Success)

    def pushErrorMessage(self, message):
        self.messageBar.pushMessage("Error", message, level=Qgis.Critical)


class MainForm(Form):
    def __init__(self, manager, parent=None):
        super().__init__("main.ui", MainPresenter, manager, parent)
        self.imageLayerComboBox.currentIndexChanged.connect(self.imageryLayerChoose)
        self.indexLayerComboBox.currentIndexChanged.connect(self.indexLayerChoose)
        self.paramsButton.clicked.connect(self.openParamsWidget)
        self.suppressButton.clicked.connect(self.unveilImage)

    def imageryLayerChoose(self):
        self.presenter.imagery_layer_choose(self.imageLayerComboBox.currentLayer())

    def indexLayerChoose(self):
        self.presenter.index_layer_choose(self.indexLayerComboBox.currentLayer())

    def unveilImage(self):
        result_path = QFileDialog.getSaveFileName(self)[0]
        self.imageryLayerChoose()
        self.indexLayerChoose()
        self.presenter.unveil_image(result_path, self.manager.parameters)

    def addLayerToPanel(self, layer):
        QgsProject.instance().addMapLayer(layer)

    def openParamsWidget(self):
        self.manager.params_widget.show()


class ParamsForm(Form):
    def __init__(self, manager, parent=None):
        super().__init__("params.ui", ParamsPresenter, manager, parent)
        self.scalingCheckBox.toggled.connect(
            partial(self.checkbox_toggled, (self.scaleFromSpinBox, self.scaleToSpinBox))
        )
        self.binsCheckBox.toggled.connect(
            partial(self.checkbox_toggled, (self.binXSpinBox, self.binYSpinBox))
        )
        self.thresholdsCheckBox.toggled.connect(
            partial(self.checkbox_toggled, (self.thresholdBottomSpinBox, self.thresholdTopSpinBox))
        )
        self.maskCheckBox.toggled.connect(
            partial(self.checkbox_toggled, (self.maskLayerComboBox,))
        )
        self.scaleFromSpinBox.valueChanged.connect(self.change_range)
        self.windowAddButton.clicked.connect(self.addWindowSize)
        self.windowsClearButton.clicked.connect(self.clearWindowSizes)
        self.applyButton.clicked.connect(self.applyParameters)

    def applyParameters(self):
        try:
            self.presenter.apply_parameters(self.manager.parameters)
        except:
            self.pushErrorMessage("Parameters have not applied")
        else:
            self.pushSuccessMessage("Parameters have applied")

    def clearWindowSizes(self):
        self.presenter.clear_window_sizes()

    def addWindowSize(self):
        self.presenter.add_window_size(self.windowSpinBox.value())

    def change_range(self, value):
        self.scaleToSpinBox.setMinimum(value+self.scaleToSpinBox.singleStep())

    def checkbox_toggled(self, controls, state):
        for control in controls:
            control.setEnabled(state)

    def showEvent(self, e):
        self.presenter.init_window(self.manager.parameters)
        QWidget.showEvent(self, e)
