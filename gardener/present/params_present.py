from qgis.PyQt.QtCore import Qt
from qgis.core import QgsMessageLog, Qgis

from gardener.helpers import logger as log
from gardener.helpers.exceptions import *
from gardener.helpers import controller as check


class ParamsPresenter:
    def __init__(self, view):
        self.view = view
        self.smoothing_windows = []
        self.s = ' '

    def add_window_size(self, size):
        self.smoothing_windows.append(size)
        current_text = self.view.windowsLineEdit.text()
        new_text = str(size) if current_text == "" else self.s+str(size)
        self.view.windowsLineEdit.setText(current_text+new_text)

    def clear_window_sizes(self):
        self.smoothing_windows.clear()
        self.view.windowsLineEdit.clear()

    def apply_parameters(self, params):
        scales = None
        thresholds = None
        windows = tuple(self.smoothing_windows)
        coefficient = self.view.targetSpinBox.value()
        mask = None
        if self.view.scalingCheckBox.isChecked():
            scales = self.view.scaleFromSpinBox.value(), self.view.scaleToSpinBox.value()
        if self.view.thresholdsCheckBox.isChecked():
            thresholds = self.view.thresholdBottomSpinBox.value(), self.view.thresholdTopSpinBox.value()
        if self.view.maskCheckBox.isChecked():
            mask = self.view.maskLayerComboBox.currentLayer()
        try:
            if scales: check.scales(scales)
            if thresholds: check.thresholds(thresholds)
            check.windows(windows)
            check.coefficient(coefficient)
            if mask: check.layer(mask)
        except (ParametersError, LayersError) as e:
            log.warning(str(e))
            self.view.pushWarningMessage(str(e))
        else:
            params.scales = scales
            params.thresholds = thresholds
            params.windows = windows
            params.coefficient = coefficient
            params.mask = mask
            message = "Parameters have applied"
            log.success(message)
            self.view.pushSuccessMessage(message)

    def init_window(self, params):
        if params.scales is None:
            self.view.scalingCheckBox.setChecked(Qt.Unchecked)
        else:
            self.view.scalingCheckBox.setChecked(Qt.Checked)
            scalefrom, scaleto = params.scales
            self.view.scaleFromSpinBox.setValue(scalefrom)
            self.view.scaleToSpinBox.setValue(scaleto)
        if params.thresholds is None:
            self.view.thresholdsCheckBox.setChecked(Qt.Unchecked)
        else:
            self.view.thresholdsCheckBox.setChecked(Qt.Checked)
            bottom, top = params.thresholds
            self.view.thresholdBottomSpinBox.setValue(bottom)
            self.view.thresholdTopSpinBox.setValue(top)
        if params.mask is None:
            self.view.maskCheckBox.setChecked(Qt.Unchecked)
        else:
            self.view.maskCheckBox.setChecked(Qt.Checked)
            self.view.maskLayerComboBox.setLayer(params.mask)
        self.view.targetSpinBox.setValue(params.coefficient)
        self.smoothing_windows = list(params.windows)
        self.view.windowsLineEdit.setText(self.s.join(map(str, params.windows)))
