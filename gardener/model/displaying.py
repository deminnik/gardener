import numpy as np

from .unveiling import ForcedInvariance


class Plot:
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
    def __init__(self, data):
        self._x = np.array(list(data.keys()))
        self._y = np.array(data[key] for key in self._x)


class Cloud(Plot):
    def __init__(self, band, index):
        self._x = np.ravel(index)
        self._y = np.ravel(band)


class ForcedInvariancePlot(ForcedInvariance):
    def __call__(self, band, imagery):
        if self.params.scales is not None:
            index_scales = imagery.index.min(), imagery.index.max()
            imagery.index = self.scaling(imagery.index, index_scales, self.params.scales)
        if self.params.bins is not None:
            self.compression(imagery.index, self.params.bins[1])
        temp = imagery[band]
        if self.params.scales is not None:
            scales = temp.min(), temp.max()
            temp = self.scaling(temp, scales, self.params.scales)
        if self.params.bins is not None:
            self.compression(temp, self.params.bins[0])
        stat = self.statistics(temp, imagery.index)
        curve = self.correlation(stat)
        self.smoothing(curve)
        return Curve(curve), Cloud(temp, imagery.index)
