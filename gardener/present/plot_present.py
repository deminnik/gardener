from gardener.model.unveiling import Imagery
from gardener.model.displaying import ForcedInvariancePlot

from gardener.helpers.tasks import PlotTask
from gardener.helpers import logger as log
from gardener.helpers.exceptions import *
from gardener.helpers import controller as check


class PlotPresenter:
    def __init__(self, view):
        self.view = view

    def get_statistics(self, band, imagery, index, params):
        try:
            check.layer(imagery)
            check.layer(index)
            check.sizes(imagery, index)
        except (LayersError, SizesError) as e:
            log.warning(str(e))
            self.view.pushWarningMessage(str(e))
        else:
            image = Imagery(imagery.source(), index_path=index.source())
            fim = ForcedInvariancePlot(params)
            plot_task = PlotTask(imagery.name(), f"Band {band}", index.name())
            plot_task.presenter(self)
            plot_task.configure(fim, band, image)
            self.view.manager.task_manager.addTask(plot_task)

    def displaying_finished(self, band, frame):
        self.view.addTab(frame, f"Band {band}")
        message = "Displaying completed"
        log.info(message)
        self.view.pushInfoMessage(message)

    def displaying_error(self):
        message = "Displaying was interrupted"
        log.error(message)
        self.view.pushErrorMessage(message)
