from qgis.PyQt.QtCore import Qt
from qgis.core import QgsMessageLog, Qgis


class ParamsPresenter:
    def __init__(self, view):
        self.view = view

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
        self.view.targetSpinBox.setValue(params.coefficient)
        self.view.windowsLineEdit.setText(", ".join(map(str, params.windows)))
