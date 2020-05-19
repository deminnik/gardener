"""forms.py
Gardener - plugin for QGIS
Copyright (C) 2020  Nikita Demin
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
from os import path
from functools import partial

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget, QFileDialog, QVBoxLayout, QMessageBox
from qgis.PyQt.QtCore import Qt
from qgis.core import Qgis
from qgis.core import QgsProject

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from gardener.present.main_present import MainPresenter
from gardener.present.params_present import ParamsPresenter
from gardener.present.plot_present import PlotPresenter
from gardener.present.test_present import TestPresenter

from gardener.helpers import logger as log


class Form(QWidget):
    def __init__(self, uifile, presenter, manager, parent=None):
        super().__init__(parent=parent, flags=Qt.Window)
        uipath = "ui"
        ui = path.join(path.dirname(__file__), f"{uipath}/{uifile}")
        uic.loadUi(ui, self)
        self.manager = manager
        self.presenter = presenter(self)
        self.messageBar = self.manager.iface.messageBar()
        self.messageTitle = "Gardener plugin"

    def saveFileDialog(self, driver="All Files", extension=".*"):
        title = "File save"
        directory = QgsProject.instance().homePath()
        filters = f"{driver} (*{extension})"
        result = QFileDialog.getSaveFileName(self, title, directory, filters)[0]
        if result:
            if extension != ".*" and result[-len(extension):] != extension:
                result += extension
            return result
        else:
            return ""

    def toggleControlState(self, controls, state):
        for control in controls:
            control.setEnabled(state)

    def pushSuccessMessage(self, message):
        self.messageBar.pushMessage(self.messageTitle, message, level=Qgis.Success)

    def pushInfoMessage(self, message):
        self.messageBar.pushMessage(self.messageTitle, message, level=Qgis.Info)

    def pushWarningMessage(self, message):
        self.messageBar.pushMessage(self.messageTitle, message, level=Qgis.Warning)

    def pushErrorMessage(self, message):
        self.messageBar.pushMessage(self.messageTitle, message, level=Qgis.Critical)


class MainForm(Form):
    def __init__(self, manager, layers_count, parent=None):
        super().__init__("main.ui", MainPresenter, manager, parent)
        self.imageLayerComboBox.currentIndexChanged.connect(self.imageryLayerChoose)
        self.imageLayerComboBox.currentIndexChanged.connect(self.layerAdd)
        self.indexLayerComboBox.currentIndexChanged.connect(self.indexLayerChoose)
        self.paramsButton.clicked.connect(self.openParamsWidget)
        self.suppressButton.clicked.connect(self.unveilImage)
        self.showButton.clicked.connect(self.openPlotWidget)
        self.testButton.clicked.connect(self.openTestWidget)
        if not self.imageLayerComboBox.currentLayer() is None:
            self.imageryLayerChoose()
        if not layers_count:
            self.toggleControlState((self.suppressButton, self.showButton, self.testButton), False)

    def layerAdd(self):
        count = self.imageLayerComboBox.count()
        state = True if count else False
        if state != self.suppressButton.isEnabled():
            self.toggleControlState((self.suppressButton, self.showButton, self.testButton), state)

    def imageryLayerChoose(self):
        layer = self.imageLayerComboBox.currentLayer()
        self.imageRasterBandComboBox.setLayer(layer)
        self.presenter.imagery_layer_choose(layer)

    def indexLayerChoose(self):
        self.presenter.index_layer_choose(self.indexLayerComboBox.currentLayer())

    def unveilImage(self):
        self.imageryLayerChoose()
        self.indexLayerChoose()
        self.presenter.unveil_image(self.manager.parameters)

    def addLayerToPanel(self, layer):
        QgsProject.instance().addMapLayer(layer)

    def openParamsWidget(self):
        self.manager.params_widget.show()

    def openPlotWidget(self):
        band = self.imageRasterBandComboBox.currentBand()
        imagery = self.imageLayerComboBox.currentLayer()
        index = self.indexLayerComboBox.currentLayer()
        self.manager.plot_widget.plotStatistics(band, imagery, index, self.manager.parameters)

    def openTestWidget(self):
        self.manager.test_widget.show()

    def closeEvent(self, e):
        try:
            self.manager.exitPlugin()
        except Exception as e:
            self.pushErrorMessage(str(e))
            log.error(str(e))
            e.ignore()
        else:
            e.accept()
            QWidget.closeEvent(self, e)


class ParamsForm(Form):
    def __init__(self, manager, parent=None):
        super().__init__("params.ui", ParamsPresenter, manager, parent)
        self.scalingCheckBox.setToolTip("Unfinished feature")
        self.scalingCheckBox.toggled.connect(
            partial(self.toggleControlState, (self.scaleFromSpinBox, self.scaleToSpinBox))
        )
        self.thresholdsCheckBox.toggled.connect(
            partial(self.toggleControlState, (self.thresholdBottomSpinBox, self.thresholdTopSpinBox))
        )
        self.maskCheckBox.toggled.connect(
            partial(self.toggleControlState, (self.maskLayerComboBox,))
        )
        self.scaleFromSpinBox.valueChanged.connect(self.change_range)
        self.windowAddButton.clicked.connect(self.addWindowSize)
        self.windowsClearButton.clicked.connect(self.clearWindowSizes)
        self.applyButton.clicked.connect(self.applyParameters)

    def applyParameters(self):
        self.presenter.apply_parameters(self.manager.parameters)

    def clearWindowSizes(self):
        self.presenter.clear_window_sizes()

    def addWindowSize(self):
        self.presenter.add_window_size(self.windowSpinBox.value())

    def change_range(self, value):
        self.scaleToSpinBox.setMinimum(value+self.scaleToSpinBox.singleStep())

    def showEvent(self, e):
        self.presenter.init_window(self.manager.parameters)
        QWidget.showEvent(self, e)


class PlotForm(Form):

    class PlotFrame(QWidget):
        def __init__(self, curve, cloud, parent=None):
            super().__init__(parent)
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            self.toolbar = NavigationToolbar(self.canvas, self)
            self.set_layout()
            self.set_figure()
            self.plot_cloud(cloud)
            self.plot_curve(curve)
            self.canvas.draw()

        def set_layout(self):
            vbox = QVBoxLayout()
            vbox.addWidget(self.canvas)
            vbox.addWidget(self.toolbar)
            self.setLayout(vbox)

        def set_figure(self):
            self.axes = self.figure.add_subplot(111)
            self.axes.clear()

        def plot_curve(self, curve):
            self.axes.plot(curve.x, curve.y, linewidth=0.5, color='k')

        def plot_cloud(self, cloud):
            self.axes.scatter(cloud.x, cloud.y, s=0.2, c='y')
            

    def __init__(self, manager, parent=None):
        super().__init__("plot.ui", PlotPresenter, manager, parent)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

    def plotStatistics(self, band, imagery, index, params):
        self.presenter.get_statistics(band, imagery, index, params)

    def addTab(self, content, title):
        self.tabWidget.addTab(content, title)
        self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
        self.show()

    def closeTab(self, index):
        self.tabWidget.removeTab(index)


class TestForm(Form):
    def __init__(self, manager, parent=None):
        super().__init__("test.ui", TestPresenter, manager, parent)
        self.imageryLayerComboBox.currentIndexChanged.connect(self.imageryLayerChoose)
        self.imageryLayerComboBox.currentIndexChanged.connect(self.layerAdd)
        self.indexLayerComboBox.currentIndexChanged.connect(self.indexLayerChoose)
        self.standardLayerComboBox.currentIndexChanged.connect(self.standardLayerChoose)
        self.thresholdSpinBox.valueChanged.connect(self.thresholdValueChange)
        self.testButton.clicked.connect(self.testAlgorithm)

    def layerAdd(self):
        count = self.imageryLayerComboBox.count()
        state = True if count else False
        if state != self.testButton.isEnabled():
            self.toggleControlState((self.testButton,), state)

    def testAlgorithm(self):
        self.imageryLayerChoose()
        self.indexLayerChoose()
        self.standardLayerChoose()
        self.thresholdValueChange()
        self.presenter.test_algorithm()

    def showTestResult(self, result):
        self.resultNumber.display(result)

    def imageryLayerChoose(self):
        self.presenter.imagery_layer_choose(self.imageryLayerComboBox.currentLayer())

    def indexLayerChoose(self):
        self.presenter.index_layer_choose(self.indexLayerComboBox.currentLayer())

    def standardLayerChoose(self):
        self.presenter.standard_layer_choose(self.standardLayerComboBox.currentLayer())

    def thresholdValueChange(self):
        self.presenter.threshold_value_change(self.thresholdSpinBox.value())
