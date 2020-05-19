"""gardener.py
Gardener - plugin for QGIS
Copyright (C) 2020  Nikita Demin
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
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
