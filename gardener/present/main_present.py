from qgis.core import QgsTask
from gardener.model.unveiling import ForcedInvariance


class FImTask(QgsTask):
    def __init__(self, fim, args):
        super().__init__("Task for FIM", QgsTask.CanCancel)
        self.fim = fim
        self.image, self.index = args
    
    def run(self):
        try:
            self.fim(self.image, self.index)
        except:
            return False
        else:
            return True


class MainPresenter:
    def __init__(self, view):
        self.view = view

    def suppress_vegetation(self, params):
        import numpy as np
        image = np.array([[[1,2], [2,3]], [[1,2], [2,3]]])
        index = np.array([[0.2, 0.1], [1, 0.3]])
        fim = ForcedInvariance(params)
        # fim(image, index)
        fim_task = FImTask(fim, (image, index))
        fim_task.taskCompleted.connect(self.suppress_finished)
        self.view.manager.task_manager.addTask(fim_task)

    def suppress_finished(self):
        self.view.suppressFinished()
