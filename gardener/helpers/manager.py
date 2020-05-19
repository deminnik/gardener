"""manager.py
Gardener - plugin for QGIS
Copyright (C) 2020  Nikita Demin
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
from qgis.core import QgsApplication, QgsProject, QgsMapLayer

from gardener.view.forms import MainForm, ParamsForm, PlotForm, TestForm

from gardener.model.unveiling import Parameters


class PluginManager:
    def __init__(self, iface):
        self.iface = iface
        self.task_manager = QgsApplication.taskManager()
        self.parameters = Parameters()
        count = QgsProject.instance().count()
        self.main_widget = MainForm(self, count)
        self.params_widget = ParamsForm(self, parent=self.main_widget)
        self.plot_widget = PlotForm(self, parent=self.main_widget)
        self.test_widget = TestForm(self, parent=self.main_widget)

    def exitPlugin(self):
        self.params_widget.close()
        self.plot_widget.close()
        self.test_widget.close()
