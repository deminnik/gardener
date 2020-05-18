import gdal

from qgis.core import QgsMapLayer

from .exceptions import *


def layer(layer):
    if layer is None:
        raise LayersError("No layer selected")
    if layer.type() != QgsMapLayer.LayerType.RasterLayer:
        raise LayersError("Layer type is not 'raster layer'")

def sizes(*args):
    sizes = []
    for item in args:
        image = gdal.Open(item.source())
        size = image.RasterXSize, image.RasterYSize
        sizes.append(size)
    if len(set(sizes)) != 1:
        raise SizesError("Rasters have different sizes")

def scales(scales):
    if scales[0] >= scales[1]:
        raise ParametersError("In scales from >= to")

def thresholds(thresholds):
    if thresholds[0] >= thresholds[1]:
        raise ParametersError("In thresholds bottom >= top")

def windows(windows):
    if not windows:
        raise ParametersError("At least one window for the median filter is required")
    if not all(map(lambda x: x > 1, windows)):
        raise ParametersError("Some window sizes less than or equal 1")

def coefficient(coefficient):
    if coefficient <= 0:
        raise ParametersError("Target value coefficient must be a positive number")

def test_threshold(threshold):
    if 1 < threshold < 0:
        raise ParametersError("Threshold value must be in range [0, 1]")
