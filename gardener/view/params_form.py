from os import path
from functools import partial

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtCore import Qt


class ParamsForm(QWidget):
    def __init__(self, manager, parent=None):
        super(ParamsForm, self).__init__(parent)
        self.uifile = path.join(path.dirname(__file__), "ui/params.ui")
        self.manager = manager
        uic.loadUi(self.uifile, self)
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
        self.init_window(self.manager.parameters)

    def init_window(self, params):
        if params.scales is None:
            self.scalingCheckBox.setChecked(Qt.Unchecked)
        else:
            self.scalingCheckBox.setChecked(Qt.Checked)
            self.scaleFromSpinBox.setValue(params.scales[0])
            self.scaleToSpinBox.setValue(params.scales[1])
        if params.bins is None:
            self.binsCheckBox.setChecked(Qt.Unchecked)
        else:
            self.binsCheckBox.setChecked(Qt.Checked)
            self.binXSpinBox.setValue(params.bins[0])
            self.binYSpinBox.setValue(params.bins[1])
        if params.thresholds is None:
            self.thresholdsCheckBox.setChecked(Qt.Unchecked)
        else:
            self.thresholdsCheckBox.setChecked(Qt.Checked)
            self.binXSpinBox.setValue(params.thresholds[0])
            self.binYSpinBox.setValue(params.thresholds[1])
        if params.mask is None:
            self.maskCheckBox.setChecked(Qt.Unchecked)
        else:
            self.maskCheckBox.setChecked(Qt.Checked)
            self.maskLayerComboBox.setLayer(params.mask)
        self.targetSpinBox.setValue(params.coefficient)
        self.windowsLineEdit.setText(", ".join(map(str, params.windows)))

    def checkbox_toggled(self, controls, state):
        for control in controls:
            control.setEnabled(state)
