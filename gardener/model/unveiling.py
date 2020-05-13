from scipy.signal import medfilt
from collections import defaultdict
import numpy as np


class Parameters:
    def __init__(self):
        self.__scales = None
        self.__bins = None
        self.__thresholds = None
        self.__windows = (3,)
        self.__coefficient = 1.0
        self.__mask = None

    def get_scales(self):
        return self.__scales

    def set_scales(self, scales):
        self.__scales = scales

    def get_bins(self):
        return self.__bins

    def set_bins(self, bins):
        self.__bins = bins

    def get_thresholds(self):
        return self.__thresholds

    def set_thresholds(self, thresholds):
        self.__thresholds = thresholds

    def get_windows(self):
        return self.__windows

    def set_windows(self, windows):
        self.__windows = windows

    def get_coefficient(self):
        return self.__coefficient

    def set_coefficient(self, coefficient):
        self.__coefficient = coefficient

    def get_mask(self):
        return self.__mask

    def set_mask(self, mask):
        self.__mask = mask
    
    scales = property(get_scales, set_scales)
    bins = property(get_bins, set_bins)
    thresholds = property(get_thresholds, set_thresholds)
    windows = property(get_windows, set_windows)
    coefficient = property(get_coefficient, set_coefficient)
    mask = property(get_mask, set_mask)

class ForcedInvariance:
    def __init__(self, parameters):
        self.params = parameters

    def __call__(self, image, index):
        if self.params.scales is not None:
            index = self.scaling(index, (index.min(), index.max()), self.params.scales)
        if self.params.bins is not None:
            self.compression(index, self.params.bins[1])
        for band in image:
            temp = band.copy()
            scales = None
            if self.params.scales is not None:
                scales = temp.min(), temp.max()
                temp = self.scaling(temp, scales, self.params.scales)
            if self.params.bins is not None:
                self.compression(temp, self.params.bins[0])
            stat = self.statistics(temp, index)
            curve = self.correlation(stat)
            target = self.target_value(temp)
            del temp
            self.recalculate(band, curve, index, target, scales)

    def scaling(self, value, old, new):
        omin, omax = old
        nmin, nmax = new
        orange = omax - omin
        nrange = nmax - nmin
        return ((value - omin) / orange) * nrange + nmin

    def compression(self, raster, step):
        values = np.sort(np.ravel(raster)).reshape(-1, step)
        mean = values.mean(axis=1)
        for i in range(len(mean)):
            for value in values[i]:
                indexes = np.argwhere(raster==value)
                iy = [x[0] for x in indexes]
                ix = [x[1] for x in indexes]
                raster[iy, ix] = mean[i]

    def statistics(self, band, index):
        stat = defaultdict(list)
        y, x = band.shape
        for i in range(y):
            for j in range(x):
                stat[index[i, j]].append(band[i, j])
        return stat

    def correlation(self, stat):
        curve = {i:round(sum(stat[i])/len(stat[i])) for i in stat}
        self.smoothing(curve)
        return curve

    def smoothing(self, curve):
        keys = sorted(curve.keys())
        values = [curve[key] for key in keys]
        for window in self.params.windows:
            values = medfilt(values, window)
        curve = dict(zip(keys, values))

    def target_value(self, band):
        return band.mean() * self.params.coefficient

    def recalculate(self, band, curve, index, target, scales):
        def curve_value(value):
            nonlocal scales
            if scales is not None:
                value = self.scaling(value, self.params.scales, scales)
            return value if value != 0 else 1
        y, x = band.shape
        for i in range(y):
            for j in range(x):
                band[i, j] *= target / curve_value(curve[index[i, j]])
