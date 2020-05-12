from os import path
from functools import partial

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget
from qgis.core import Qgis

from gardener.present.params_present import ParamsPresenter


class ParamsForm(QWidget):
    def __init__(self, manager, parent=None):
        super(ParamsForm, self).__init__(parent)
        self.uifile = path.join(path.dirname(__file__), "ui/params.ui")
        self.manager = manager
        self.presenter = ParamsPresenter(self)
        uic.loadUi(self.uifile, self)
        self.messageBar = self.manager.iface.messageBar()
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
            self.messageBar.pushMessage("Error", "Parameters have not applied", level=Qgis.Critical)
        else:
            self.messageBar.pushMessage("Success", "Parameters have applied", level=Qgis.Success)

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
