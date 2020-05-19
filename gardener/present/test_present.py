from qgis.PyQt.QtWidgets import QFileDialog

from gardener.model.unveiling import Imagery, Raster, ForcedInvariance
from gardener.model.evaluating import Comparator

from gardener.helpers.tasks import TestTask
from gardener.helpers import logger as log
from gardener.helpers.exceptions import *
from gardener.helpers import controller as check


class TestPresenter:
    def __init__(self, view):
        self.view = view

    def test_algorithm(self):
        try:
            check.layer(self.imagery_layer)
            check.layer(self.index_layer)
            check.layer(self.standard_layer)
            check.sizes(self.imagery_layer, self.index_layer, self.standard_layer)
            check.test_threshold(self.threshold)
        except (LayersError, SizesError, ParametersError) as e:
            log.warning(str(e))
            self.view.pushWarningMessage(str(e))
        else:
            imagery = Imagery(self.imagery_layer.source(), 
                        index_path=self.index_layer.source())
            unveiled = self.view.saveFileDialog(extension=imagery.extension, 
                                                driver=imagery.driver)
            if unveiled:
                imagery.unveiled(unveiled)
                standard = Raster(self.standard_layer.source())
                fim = ForcedInvariance(self.view.manager.parameters)
                comparator = Comparator(self.threshold)
                test_task = TestTask(self.imagery_layer.name(), self.standard_layer.name())
                test_task.presenter(self)
                test_task.configure(comparator, fim, imagery, standard, unveiled)
                self.view.manager.task_manager.addTask(test_task)

    def testing_finished(self, result):
        self.view.showTestResult(result)
        message = "Testing completed"
        log.info(message)
        self.view.pushSuccessMessage(message)

    def testing_error(self):
        message = "Testing was interrupted"
        log.error(message)
        self.view.pushErrorMessage(message)

    def imagery_layer_choose(self, layer):
        self.imagery_layer = layer

    def index_layer_choose(self, layer):
        self.index_layer = layer

    def standard_layer_choose(self, layer):
        self.standard_layer = layer

    def threshold_value_change(self, value):
        self.threshold = value
