from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction


class Gardener:
    def __init__(self, iface):
        self.iface = iface

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
        pass
