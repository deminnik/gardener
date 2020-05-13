from qgis.core import QgsTask
from gardener.model.unveiling import ForcedInvariance, Imagery


class FImTask(QgsTask):
    def __init__(self, image_name, index_name):
        title = "Unveiling by FIM"
        layers = f"image('{image_name}'), index('{index_name}')"
        name = f"{title}: {layers}"
        super().__init__(name, QgsTask.CanCancel)

    def configure(self, algorithm, argument):
        self.__fim = algorithm
        self.__img = argument
    
    def run(self):
        try:
            self.__fim(self.__img)
        except:
            return False
        else:
            return True


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
        fim = ForcedInvariance(params)
        fim_task = FImTask(self.__imagery_layer.name(), 
                           self.__index_layer.name())
        fim_task.configure(fim, image)
        fim_task.taskCompleted.connect(self.unveiling_finished)
        self.view.manager.task_manager.addTask(fim_task)

    def unveiling_finished(self):
        self.view.unveilingFinished()
