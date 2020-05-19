import unittest

import numpy as np

from gardener.model.evaluating import Comparator


class SimilarityMeasureMethod(unittest.TestCase):
    def test_similarity_measure_basic(self):
        image = np.array([[[0.1, 0.1],
                           [0.7, 0.8]],
                          [[0.4, 0.8],
                           [0.2, 0.6]]])
        model = np.array([[[0.5, 0.4],
                           [0.6, 0.3]],
                          [[0.3, 0.1],
                           [0.6, 0.7]]])
        check_result = np.array([[[0.57, 0.43],
                                  [0.14, 0.71]],
                                 [[0.14, 1.0],
                                  [0.57, 0.14]]])
        result = np.around(Comparator.similarity_measure(None, image, model), 2)
        self.assertTrue(np.array_equal(result, check_result))


class DistanceCalculationMethod(unittest.TestCase):
    def test_distance_calculation_basic(self):
        cube = np.array([[[0.9, 0.2],
                         [0.3, 0.4]],
                         [[0.5, 0.4],
                         [0.1, 0.6]]])
        check_result = np.array([[0.7, 0.3],
                                 [0.2, 0.5]])
        result = np.around(Comparator.distance_calculation(None, cube), 1)
        self.assertTrue(np.array_equal(result, check_result))


class SimilarityFilterMethod(unittest.TestCase):
    def setUp(self):
        self.comparator = Comparator(0.3)

    def test_similarity_filter_basic(self):
        matrix = np.array([[0.2, 0.3],
                           [0.4, 0.1]])
        check_result = np.array([[True, True],
                                 [False, True]])
        result = self.comparator.similarity_filter(matrix)
        self.assertTrue(np.array_equal(result, check_result))


class SimilarityCalculationMethod(unittest.TestCase):
    def test_similarity_calculation_basic(self):
        matrix = np.array([[True, True],
                           [False, True]])
        check_result = 0.75
        result = Comparator.similarity_calculation(None, matrix)
        self.assertAlmostEqual(result, check_result)
