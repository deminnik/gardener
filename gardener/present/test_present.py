from qgis.PyQt.QtWidgets import QFileDialog

from gardener.model.unveiling import Imagery, Raster, ForcedInvariance
from gardener.model.evaluating import Comparator

from gardener.helpers.tasks import TestTask


class TestPresenter:
    def __init__(self, view):
        self.view = view

    def test_algorithm(self):
        unveiled = QFileDialog.getSaveFileName(self.view)[0]
        imagery = Imagery(self.__imagery_layer.source(), 
                      index_path=self.__index_layer.source())
        imagery.unveiled(unveiled)
        standard = Raster(self.__standard_layer.source())
        fim = ForcedInvariance(self.view.manager.parameters)
        comparator = Comparator(self.__threshold)
        test_task = TestTask(self.__imagery_layer.name(), self.__standard_layer.name())
        test_task.presenter(self)
        test_task.configure(comparator, fim, imagery, standard, unveiled)
        self.view.manager.task_manager.addTask(test_task)

    def testing_finished(self, result):
        self.view.showTestResult(result)
        self.view.pushSuccessMessage("Testing completed")

    def testing_error(self):
        self.view.pushErrorMessage("Testing was interrupted")

    def imagery_layer_choose(self, layer):
        self.__imagery_layer = layer

    def index_layer_choose(self, layer):
        self.__index_layer = layer

    def standard_layer_choose(self, layer):
        self.__standard_layer = layer

    def threshold_value_change(self, value):
        self.__threshold = value
