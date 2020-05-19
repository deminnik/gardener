"""evaluating.py
Gardener - plugin for QGIS
Copyright (C) 2020  Nikita Demin
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
import numpy as np


class Comparator:
    """Comparison with a standard method
    Args:
        threshold (float): threshold for similarity filter
    Attributes:
        _threshold (float): threshold for similarity filter
    """
    def __init__(self, threshold):
        self._threshold = threshold

    def __call__(self, image, model):
        """Comparison with a standard
        Args:
            image (numpy.ndarray): processed imagery
            model (numpy.ndarray): standard imagery
        Returns:
            float: similarity value
        """
        if image.ndim == 3 and model.ndim == 3:
            simcube = self.similarity_measure(image, model)
            distmatrix = self.distance_calculation(simcube)
            simmatrix = self.similarity_filter(distmatrix)
            similarity = self.similarity_calculation(simmatrix)
            return similarity

    def similarity_measure(self, image, model):
        """Сalculation similarity measure for imagery bands
        Args:
            image (numpy.ndarray): processed imagery
            model (numpy.ndarray): standard imagery
        Returns:
            numpy.ndarray: similarity measure for each band
        """
        ncube = np.empty(image.shape)
        k = image.shape[0]
        for i in range(k):
            max_dn = max(image[i].max(), model[i].max())
            min_dn = min(image[i].min(), model[i].min())
            ncube[i] = max_dn - min_dn
        return np.absolute(image - model) / ncube

    def distance_calculation(self, cube):
        """Hamming distance calculation
        Args:
            cube (numpy.ndarray): similarity measure for each band
        Returns:
            numpy.ndarray: Hamming distance for each pixel
        """
        weights = np.ones(cube.shape) / cube.shape[0]
        return np.sum(cube * weights, axis=0)

    def similarity_filter(self, matrix):
        """Hamming distance filtering 
        Args:
            matrix (numpy.ndarray): Hamming distance for each pixel
        Returns:
            numpy.ndarray: boolean array
        """
        return matrix <= self._threshold

    def similarity_calculation(self, matrix):
        """Calculating similarity between imageries
        Args:
            matrix (numpy.ndarray): boolean array
        Returns:
            float: similarity
        """
        clear_pixels = np.count_nonzero(matrix)
        all_pixels = matrix.shape[0] * matrix.shape[1]
        return clear_pixels / all_pixels
