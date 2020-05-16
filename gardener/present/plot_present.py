from qgis.core import QgsTask

from gardener.model.unveiling import Imagery
from gardener.model.displaying import ForcedInvariancePlot

from gardener.helpers import logger as log


class PlotTask(QgsTask):
    def __init__(self, image_name, band_name, index_name):
        title = "Statistics by FIM"
        layers = f"image('{image_name}', band('{band_name}')), index('{index_name}')"
        name = f"{title}: {layers}"
        super().__init__(name, QgsTask.CanCancel)

    def presenter(self, presenter):
        self.__presenter = presenter

    def configure(self, algorithm, band, imagery):
        self.__fim = algorithm
        self.__band = band
        self.__img = imagery
    
    def run(self):
        try:
            self.__curve, self.__cloud = self.__fim(self.__band, self.__img)
        except Exception as e:
            raise e
        else:
            return True

    def finished(self, result):
        if result:
            frame = self.__presenter.view.PlotFrame(self.__curve, self.__cloud)
            self.__presenter.displaying_finished(self.__band, frame)

    def cancel(self):
        self.__presenter.displaying_error()
        super().cancel()


class PlotPresenter:
    def __init__(self, view):
        self.view = view

    def get_statistics(self, band, imagery, index, params):
        image = Imagery(imagery.source(), index_path=index.source())
        fim = ForcedInvariancePlot(params)
        plot_task = PlotTask(imagery.name(), f"Band {band}", index.name())
        plot_task.presenter(self)
        plot_task.configure(fim, band, image)
        self.view.manager.task_manager.addTask(plot_task)

    def displaying_finished(self, band, frame):
        self.view.addTab(frame, f"Band {band}")
        self.view.pushSuccessMessage("Displaying completed")

    def displaying_error(self):
        self.view.pushErrorMessage("Displaying was interrupted")
