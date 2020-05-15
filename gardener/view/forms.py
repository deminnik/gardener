from os import path
from functools import partial

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget, QFileDialog, QVBoxLayout
from qgis.core import Qgis
from qgis.core import QgsProject

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from gardener.present.main_present import MainPresenter
from gardener.present.params_present import ParamsPresenter
from gardener.present.plot_present import PlotPresenter


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
        self.showButton.clicked.connect(self.openPlotWidget)

    def imageryLayerChoose(self):
        layer = self.imageLayerComboBox.currentLayer()
        self.imageRasterBandComboBox.setLayer(layer)
        self.presenter.imagery_layer_choose(layer)

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

    def openPlotWidget(self):
        band = self.imageRasterBandComboBox.currentBand()
        imagery = self.imageLayerComboBox.currentLayer()
        index = self.indexLayerComboBox.currentLayer()
        self.manager.plot_widget.plotStatistics(band, imagery, index, self.manager.parameters)


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


class PlotForm(Form):

    class PlotFrame(QWidget):
        def __init__(self, curve, parent=None):
            super().__init__(parent)
            self.__figure = Figure()
            self.__canvas = FigureCanvas(self.__figure)
            self.__toolbar = NavigationToolbar(self.__canvas, self)
            self.__set_layout()
            self.__set_figure()
            self.__plot_curve(curve)
            self.__canvas.draw()

        def __set_layout(self):
            vbox = QVBoxLayout()
            vbox.addWidget(self.__canvas)
            vbox.addWidget(self.__toolbar)
            self.setLayout(vbox)

        def __set_figure(self):
            self.__axes = self.__figure.add_subplot(111)
            self.__axes.clear()

        def __plot_curve(self, curve):
            self.__axes.plot(curve[0], curve[1], linewidth=1, color='k')
            

    def __init__(self, manager, parent=None):
        super().__init__("plot.ui", PlotPresenter, manager, parent)

    def plotStatistics(self, band, imagery, index, params):
        self.presenter.get_statistics(band, imagery, index, params)

    def addTab(self, content, title):
        self.tabWidget.addTab(content, title)
        self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
        self.show()
