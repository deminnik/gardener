from qgis.PyQt.QtCore import Qt
from qgis.core import QgsMessageLog, Qgis


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
                QgsMessageLog.logMessage("In scales from >= to", "Gardener", level=Qgis.Warning)
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
                QgsMessageLog.logMessage("In thresholds bottom >= top", "Gardener", level=Qgis.Warning)
        if params.mask is None:
            self.view.maskCheckBox.setChecked(Qt.Unchecked)
        else:
            self.view.maskCheckBox.setChecked(Qt.Checked)
            self.view.maskLayerComboBox.setLayer(params.mask)
        if params.coefficient >= 0:
            self.view.targetSpinBox.setValue(params.coefficient)
        else:
            QgsMessageLog.logMessage("Target value coefficient must be a positive number", "Gardener", level=Qgis.Warning)
        if all(map(lambda x: x > 1, params.windows)):
            self.smoothing_windows = params.windows.copy()
            self.view.windowsLineEdit.setText(self.s.join(map(str, params.windows)))
        else:
            QgsMessageLog.logMessage("Some window sizes less than or equal 1", "Gardener", level=Qgis.Warning)
