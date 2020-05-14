from qgis.PyQt.QtCore import Qt
from qgis.core import QgsMessageLog, Qgis

from gardener.helpers import logger as log


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
        if self.view.scalingCheckBox.isChecked():
            params.scales = self.view.scaleFromSpinBox.value(), self.view.scaleToSpinBox.value()
        else:
            params.scales = None
        if self.view.binsCheckBox.isChecked():
            params.bins = self.view.binXSpinBox.value(), self.view.binYSpinBox.value()
        else:
            params.bins = None
        if self.view.thresholdsCheckBox.isChecked():
            params.thresholds = self.view.thresholdBottomSpinBox.value(), self.view.thresholdTopSpinBox.value()
        else:
            params.thresholds = None
        params.windows = tuple(self.smoothing_windows)
        params.coefficient = self.view.targetSpinBox.value()
        if self.view.maskCheckBox.isChecked():
            params.mask = self.view.maskLayerComboBox.currentLayer()
        else:
            params.mask = None

    def init_window(self, params):
        if params.scales is None:
            self.view.scalingCheckBox.setChecked(Qt.Unchecked)
        else:
            self.view.scalingCheckBox.setChecked(Qt.Checked)
            scalefrom, scaleto = params.scales
            if scalefrom < scaleto:
                self.view.scaleFromSpinBox.setValue(scalefrom)
                self.view.scaleToSpinBox.setValue(scaleto)
            else:
                log.warning("In scales from >= to")
        if params.bins is None:
            self.view.binsCheckBox.setChecked(Qt.Unchecked)
        else:
            self.view.binsCheckBox.setChecked(Qt.Checked)
            self.view.binXSpinBox.setValue(params.bins[0])
            self.view.binYSpinBox.setValue(params.bins[1])
        if params.thresholds is None:
            self.view.thresholdsCheckBox.setChecked(Qt.Unchecked)
        else:
            self.view.thresholdsCheckBox.setChecked(Qt.Checked)
            bottom, top = params.thresholds
            if bottom < top:
                self.view.thresholdBottomSpinBox.setValue(bottom)
                self.view.thresholdTopSpinBox.setValue(top)
            else:
                log.warning("In thresholds bottom >= top")
        if params.mask is None:
            self.view.maskCheckBox.setChecked(Qt.Unchecked)
        else:
            self.view.maskCheckBox.setChecked(Qt.Checked)
            self.view.maskLayerComboBox.setLayer(params.mask)
        if params.coefficient >= 0:
            self.view.targetSpinBox.setValue(params.coefficient)
        else:
            log.warning("Target value coefficient must be a positive number")
        if all(map(lambda x: x > 1, params.windows)):
            self.smoothing_windows = list(params.windows)
            self.view.windowsLineEdit.setText(self.s.join(map(str, params.windows)))
        else:
            log.warning("Some window sizes less than or equal 1")
