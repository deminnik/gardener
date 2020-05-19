from functools import partial
from os import path

from qgis.core import QgsRasterLayer, Qgis

from gardener.model.unveiling import ForcedInvariance, Imagery
from gardener.helpers.tasks import FImTask
from gardener.helpers import logger as log
from gardener.helpers.exceptions import *
from gardener.helpers import controller as check


class MainPresenter:
    def __init__(self, view):
        self.view = view

    def imagery_layer_choose(self, layer):
        self.imagery_layer = layer

    def index_layer_choose(self, layer):
        self.index_layer = layer

    def unveil_image(self, params):
        try:
            check.layer(self.imagery_layer)
            check.layer(self.index_layer)
            check.sizes(self.imagery_layer, self.index_layer)
        except (LayersError, SizesError) as e:
            log.warning(str(e))
            self.view.pushWarningMessage(str(e))
        else:
            image = Imagery(self.imagery_layer.source(),
                            index_path=self.index_layer.source())
            result = self.view.saveFileDialog(extension=image.extension, 
                                              driver=image.driver)
            if result:
                image.unveiled(result)
                fim = ForcedInvariance(params)
                fim_task = FImTask(self.imagery_layer.name(), 
                self.index_layer.name())
                fim_task.configure(fim, image)
                fim_task.taskCompleted.connect(partial(self.unveiling_finished, result))
                fim_task.taskTerminated.connect(self.unveiling_error)
                self.view.manager.task_manager.addTask(fim_task)

    def unveiling_finished(self, layer_source):
        layer_name = path.splitext(path.basename(layer_source))[0]
        layer = QgsRasterLayer(layer_source, layer_name)
        self.view.addLayerToPanel(layer)
        message = "Unveiling completed"
        log.success(message)
        self.view.pushSuccessMessage(message)

    def unveiling_error(self):
        message = "Unveiling was interrupted"
        log.error(message)
        self.view.pushErrorMessage(message)
