from qgis.core import QgsApplication

from gardener.view.forms import MainForm, ParamsForm, PlotForm, TestForm

from gardener.model.unveiling import Parameters


class PluginManager:
    def __init__(self, iface):
        self.iface = iface
        self.task_manager = QgsApplication.taskManager()
        self.parameters = Parameters()
        self.main_widget = MainForm(self)
        self.params_widget = ParamsForm(self, parent=self.main_widget)
        self.plot_widget = PlotForm(self, parent=self.main_widget)
        self.test_widget = TestForm(self, parent=self.main_widget)

    def exitPlugin(self):
        self.params_widget.close()
        self.plot_widget.close()
        self.test_widget.close()
