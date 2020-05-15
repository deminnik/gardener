from qgis.core import QgsTask

from gardener.model.unveiling import Imagery
from gardener.model.displaying import ForcedInvariancePlot


class PlotTask(QgsTask):
    def __init__(self, image_name, band_name, index_name):
        title = "Statistics by FIM"
        layers = f"image('{image_name}', band('{band_name}')), index('{index_name}')"
        name = f"{title}: {layers}"
        super().__init__(name, QgsTask.CanCancel)

    def configure(self, algorithm, band, imagery):
        self.__fim = algorithm
        self.__band = band
        self.__img = imagery
    
    def run(self):
        try:
            curve, cloud = self.__fim(self.__band, self.__img)
        except Exception as e:
            raise e
        else:
            return True


class PlotPresenter:
    def __init__(self, view):
        self.view = view

    def get_statistics(self, band, imagery, index, params):
        image = Imagery(imagery.source(), index_path=index.source())
        fim = ForcedInvariancePlot(params)
        plot_task = PlotTask(imagery.name(), f"Band {band}", index.name())
        plot_task.configure(fim, band, image)
        plot_task.taskCompleted.connect(self.displaying_finished)
        plot_task.taskTerminated.connect(self.displaying_error)
        self.view.manager.task_manager.addTask(plot_task)

    def displaying_finished(self):
        self.view.pushSuccessMessage("Displaying completed")

    def displaying_error(self):
        self.view.pushErrorMessage("Displaying was interrupted")
