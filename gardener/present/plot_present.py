from gardener.model.unveiling import Imagery
from gardener.model.displaying import ForcedInvariancePlot

from gardener.helpers.tasks import PlotTask


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
