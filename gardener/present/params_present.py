from qgis.PyQt.QtCore import Qt


class ParamsPresenter:
    def __init__(self, view):
        self.view = view

    def init_window(self, params):
        if params.scales is None:
            self.view.scalingCheckBox.setChecked(Qt.Unchecked)
        else:
            self.view.scalingCheckBox.setChecked(Qt.Checked)
            self.view.scaleFromSpinBox.setValue(params.scales[0])
            self.view.scaleToSpinBox.setValue(params.scales[1])
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
            self.view.binXSpinBox.setValue(params.thresholds[0])
            self.view.binYSpinBox.setValue(params.thresholds[1])
        if params.mask is None:
            self.view.maskCheckBox.setChecked(Qt.Unchecked)
        else:
            self.view.maskCheckBox.setChecked(Qt.Checked)
            self.view.maskLayerComboBox.setLayer(params.mask)
        self.view.targetSpinBox.setValue(params.coefficient)
        self.view.windowsLineEdit.setText(", ".join(map(str, params.windows)))
