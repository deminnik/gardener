from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from gardener.view.main_form import MainForm
from gardener.view.params_form import ParamsForm


class Gardener:
    def __init__(self, iface):
        self.iface = iface
        self.main_widget = MainForm(self)
        self.params_widget = ParamsForm(self)

    def initGui(self):
        self.action = QAction(
            QIcon(":/plugins/gardener/icon.png"),
            "Suppress vegetation",
            self.iface.mainWindow()
        )
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToRasterMenu("Gardener", self.action)

    def unload(self):
        self.iface.removePluginRasterMenu("Gardener", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        self.main_widget.show()
