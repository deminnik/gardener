"""tasks.py
Gardener - plugin for QGIS
Copyright (C) 2020  Nikita Demin
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
from qgis.core import QgsTask

from gardener.model.unveiling import Raster


class FImTask(QgsTask):
    def __init__(self, image_name, index_name):
        title = "Unveiling by FIM"
        layers = f"image('{image_name}'), index('{index_name}')"
        name = f"{title}: {layers}"
        super().__init__(name, QgsTask.CanCancel)

    def configure(self, algorithm, argument):
        self.fim = algorithm
        self.img = argument
    
    def run(self):
        try:
            self.fim(self.img)
        except:
            return False
        else:
            del self.img
            return True


class PlotTask(QgsTask):
    def __init__(self, image_name, band_name, index_name):
        title = "Statistics by FIM"
        layers = f"image('{image_name}', band('{band_name}')), index('{index_name}')"
        name = f"{title}: {layers}"
        super().__init__(name, QgsTask.CanCancel)

    def presenter(self, presenter):
        self.presenter = presenter

    def configure(self, algorithm, band, imagery):
        self.fim = algorithm
        self.band = band
        self.img = imagery
    
    def run(self):
        try:
            self.curve, self.cloud = self.fim(self.band-1, self.img)
        except: return False
        else: return True

    def finished(self, result):
        if result:
            frame = self.presenter.view.PlotFrame(self.curve, self.cloud)
            self.presenter.displaying_finished(self.band, frame)
        else:
            self.presenter.displaying_error()


class TestTask(QgsTask):
    def __init__(self, image_name, model_name):
        title = "Evaluating"
        layers = f"image('{image_name}'), standard('{model_name}')"
        name = f"{title}: {layers}"
        super().__init__(name, QgsTask.CanCancel)

    def presenter(self, presenter):
        self.presenter = presenter

    def configure(self, comparator, fim, imagery, standard, temp):
        self.comparator = comparator
        self.fim = fim
        self.imagery = imagery
        self.standard = standard
        self.unveiled = temp
    
    def run(self):
        try:
            self.fim(self.imagery)
            result = Raster(self.unveiled)
            self.similarity = self.comparator(result.raster, 
                                              self.standard.raster)
        except: return False
        else: return True

    def finished(self, result):
        if result:
            self.presenter.testing_finished(self.similarity)
        else:
            self.presenter.testing_error()
