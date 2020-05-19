from os import path

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from gardener.helpers.manager import PluginManager


class Gardener:
    def __init__(self, iface):
        self.iface = iface
        self.manager = PluginManager(self.iface)

    def initGui(self):
        self.action = QAction(
            QIcon(path.join(path.dirname(__file__), "logo.png")),
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
        self.manager.main_widget.show()
