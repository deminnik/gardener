from pathlib import Path
from scipy.signal import medfilt
from collections import defaultdict
import numpy as np
import numpy.ma as ma
import gdal


class Parameters:
    def __init__(self):
        self._scales = None
        self._thresholds = None
        self._windows = (3,)
        self._coefficient = 1.0
        self._mask = None

    def get_scales(self):
        return self._scales

    def set_scales(self, scales):
        self._scales = scales

    def get_thresholds(self):
        return self._thresholds

    def set_thresholds(self, thresholds):
        self._thresholds = thresholds

    def get_windows(self):
        return self._windows

    def set_windows(self, windows):
        self._windows = windows

    def get_coefficient(self):
        return self._coefficient

    def set_coefficient(self, coefficient):
        self._coefficient = coefficient

    def get_mask(self):
        return self._mask

    def set_mask(self, mask):
        self._mask = mask
    
    scales = property(get_scales, set_scales)
    thresholds = property(get_thresholds, set_thresholds)
    windows = property(get_windows, set_windows)
    coefficient = property(get_coefficient, set_coefficient)
    mask = property(get_mask, set_mask)


class Mask:
    def __init__(self, shape):
        self._array = np.full(shape, False)

    @property
    def array(self):
        return self._array

    def add(self, mask):
        self._array += mask.astype(bool)


class Image:
    def __init__(self, file):
        self._file = Path(file)
        self._image = gdal.Open(file)
        if self._image:
            self._driver = self._image.GetDriver().ShortName
        else:
            self._driver = ""
        self._extension = self._file.suffix
        self._name = self._file.stem

    @property
    def driver(self):
        return self._driver if self._driver else "Unknown"

    @property
    def name(self):
        return self._name

    @property
    def extension(self):
        return self._extension


class Raster(Image):
    def __init__(self, image_path):
        super().__init__(image_path)
        self._raster = self._image.ReadAsArray()

    def get_raster(self):
        return self._raster

    def set_raster(self, raster):
        self._raster = raster

    raster = property(get_raster, set_raster)


class Imagery(Image):
    def __init__(self, image_path, index_path):
        super().__init__(image_path)
        self._index = Raster(index_path)
        shape = self._image.RasterYSize, self._image.RasterXSize
        self._mask = Mask(shape)
        first_band = self._image.GetRasterBand(1)
        self._nodata = first_band.GetNoDataValue()
        if not self._nodata is None:
            self._mask.add(np.isin(first_band.ReadAsArray(), [self._nodata]))

    def __getitem__(self, i):
        i += 1
        if i > self._image.RasterCount:
            raise IndexError
        else:
            band = self._image.GetRasterBand(i).ReadAsArray()
            return ma.array(band, mask=self._mask.array)

    def unveiled(self, image_path):
        self._new = Image(image_path)
        bands = self._image.RasterCount
        ysize, xsize = self._image.RasterYSize, self._image.RasterXSize
        projection, transform = self._image.GetProjection(), self._image.GetGeoTransform()
        driver = self._image.GetDriver()
        metadata = driver.GetMetadata()
        if gdal.DCAP_CREATE in metadata and metadata[gdal.DCAP_CREATE] == "YES":
            self._new._image = driver.Create(image_path, xsize, ysize, bands, gdal.GDT_Float64)
            self._new._image.SetProjection(projection)
            self._new._image.SetGeoTransform(transform)
        self._counter = 1

    def save(self, band):
        self._new._image.GetRasterBand(self._counter).WriteArray(band)
        if not self._nodata is None:
            self._new._image.GetRasterBand(self._counter).SetNoDataValue(self._nodata)
        self._counter += 1

    @property
    def mask(self):
        return self._mask

    def get_index(self):
        return self._index.raster

    def set_index(self, raster):
        self._index.raster = raster

    index = property(get_index, set_index)


class ForcedInvariance:
    def __init__(self, parameters):
        self._params = parameters

    def __call__(self, imagery):
        if not self._params.mask is None:
            mask_array = gdal.Open(self._params.mask.source()).ReadAsArray()
            imagery.mask.add(mask_array)
        if not self._params.thresholds is None:
            for band in imagery:
                imagery.mask.add(imagery.index < self._params.thresholds[0])
                imagery.mask.add(imagery.index > self._params.thresholds[1])
        if self._params.scales is not None:
            index_scales = imagery.index.min(), imagery.index.max()
            imagery.index = self.scaling(imagery.index, index_scales, self._params.scales)
        for band in imagery:
            temp = band.copy()
            scales = None
            if self._params.scales is not None:
                scales = temp.min(), temp.max()
                temp = self.scaling(temp, scales, self._params.scales)
            stat = self.statistics(temp, imagery.index)
            curve = self.correlation(stat)
            curve = self.smoothing(curve)
            target = self.target_value(temp)
            del temp
            self.recalculate(band, curve, imagery.index, target, scales)
            imagery.save(band)

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
                if not band[i, j] is ma.masked:
                    stat[index[i, j]].append(band[i, j])
        return stat

    def correlation(self, stat):
        return {i:sum(stat[i])/len(stat[i]) for i in stat}

    def smoothing(self, curve):
        keys = sorted(curve.keys())
        values = [curve[key] for key in keys]
        for window in self._params.windows:
            values = medfilt(values, window)
        return dict(zip(keys, values))

    def target_value(self, band):
        return band.mean() * self._params.coefficient

    def recalculate(self, band, curve, index, target, scales):
        def curve_value(value):
            nonlocal scales
            if scales is not None:
                value = self.scaling(value, self._params.scales, scales)
            return value if value != 0 else 1
        y, x = band.shape
        for i in range(y):
            for j in range(x):
                if not band[i, j] is ma.masked:
                    band[i, j] *= target / curve_value(curve[index[i, j]])
