"""displaying.py
Gardener - plugin for QGIS
Copyright (C) 2020  Nikita Demin
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
import numpy as np

from .unveiling import ForcedInvariance


class Plot:
    """Abstract plot
    Attributes:
        _x (sequence): values for the x-axis
        _y (sequence): values for the y-axis
    """
    def __init__(self):
        self._x = tuple()
        self._y = tuple()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Curve(Plot):
    """Correlation curve"""
    def __init__(self, data):
        self._x = list(sorted(data.keys()))
        self._y = [data[key] for key in self._x]


class Cloud(Plot):
    """Cloud of points from statistics"""
    def __init__(self, band, index):
        self._x = np.ravel(index)
        self._y = np.ravel(band)


class ForcedInvariancePlot(ForcedInvariance):
    """ForcedInvariance class modification for plotting"""
    def __call__(self, band, imagery):
        """Statistics collection and curve building
        Args:
            band (int): band index in imagery
            imagery (Imagery): imagery
        Returns:
            tuple[Curve, Cloud]: correlation curve and statistics
        """
        if self._params.scales is not None:
            index_scales = imagery.index.min(), imagery.index.max()
            imagery.index = self.scaling(imagery.index, index_scales, self._params.scales)
        temp = imagery[band]
        if self._params.scales is not None:
            scales = temp.min(), temp.max()
            temp = self.scaling(temp, scales, self._params.scales)
        stat = self.statistics(temp, imagery.index)
        curve = self.correlation(stat)
        curve = self.smoothing(curve)
        return Curve(curve), Cloud(temp, imagery.index)
