from qgis.core import QgsTask

from qgis.PyQt.QtWidgets import QFileDialog

from gardener.model.unveiling import Imagery, Raster, ForcedInvariance
from gardener.model.evaluating import Comparator

from gardener.helpers import logger as log


class TestTask(QgsTask):
    def __init__(self, image_name, model_name):
        title = "Evaluating"
        layers = f"image('{image_name}'), standard('{model_name}')"
        name = f"{title}: {layers}"
        super().__init__(name, QgsTask.CanCancel)

    def presenter(self, presenter):
        self.__presenter = presenter

    def configure(self, comparator, fim, imagery, standard, temp):
        self.__comparator = comparator
        self.__fim = fim
        self.__imagery = imagery
        self.__standard = standard
        self.__unveiled = temp
    
    def run(self):
        try:
            self.__fim(self.__imagery)
            result = Raster(self.__unveiled)
            self.__similarity = self.__comparator(result.raster, 
                                                    self.__standard.raster)
        except Exception as e:
            raise e
        else:
            return True

    def finished(self, result):
        if result:
            self.__presenter.testing_finished(self.__similarity)

    def cancel(self):
        self.__presenter.testing_error()
        super().cancel()


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
