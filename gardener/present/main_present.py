from functools import partial
from os import path

from qgis.core import QgsRasterLayer, Qgis

from gardener.model.unveiling import ForcedInvariance, Imagery
from gardener.helpers.tasks import FImTask


class MainPresenter:
    def __init__(self, view):
        self.view = view

    def imagery_layer_choose(self, layer):
        self.__imagery_layer = layer

    def index_layer_choose(self, layer):
        self.__index_layer = layer

    def unveil_image(self, params):
        image = Imagery(self.__imagery_layer.source(),
                        index_path=self.__index_layer.source())
        result = self.view.saveFileDialog(extension=image.extension, 
                                          driver=image.driver)
        if result:
            image.unveiled(result)
            fim = ForcedInvariance(params)
            fim_task = FImTask(self.__imagery_layer.name(), 
                            self.__index_layer.name())
            fim_task.configure(fim, image)
            fim_task.taskCompleted.connect(
                partial(self.unveiling_finished, result)
            )
            fim_task.taskTerminated.connect(self.unveiling_error)
            self.view.manager.task_manager.addTask(fim_task)

    def unveiling_finished(self, layer_source):
        layer_name = path.splitext(path.basename(layer_source))[0]
        layer = QgsRasterLayer(layer_source, layer_name)
        self.view.addLayerToPanel(layer)
        self.view.pushSuccessMessage("Unveiling completed")

    def unveiling_error(self):
        self.view.pushErrorMessage("Unveiling was interrupted")
