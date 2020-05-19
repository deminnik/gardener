import numpy as np


class Comparator:
    def __init__(self, threshold):
        self._threshold = threshold

    def __call__(self, image, model):
        if image.ndim == 3 and model.ndim == 3:
            simcube = self.similarity_measure(image, model)
            distmatrix = self.distance_calculation(simcube)
            simmatrix = self.similarity_filter(distmatrix)
            similarity = self.similarity_calculation(simmatrix)
            return similarity

    def similarity_measure(self, image, model):
        ncube = np.empty(image.shape)
        k = image.shape[0]
        for i in range(k):
            max_dn = max(image[i].max(), model[i].max())
            min_dn = min(image[i].min(), model[i].min())
            ncube[i] = max_dn - min_dn
        return np.absolute(image - model) / ncube

    def distance_calculation(self, cube):
        weights = np.ones(cube.shape) / cube.shape[0]
        return np.sum(cube * weights, axis=0)

    def similarity_filter(self, matrix):
        return matrix <= self._threshold

    def similarity_calculation(self, matrix):
        clear_pixels = np.count_nonzero(matrix)
        all_pixels = matrix.shape[0] * matrix.shape[1]
        return clear_pixels / all_pixels
