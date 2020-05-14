import unittest

import numpy as np

from gardener.model.unveiling import ForcedInvariance, Parameters


class ScalingMethod(unittest.TestCase):
    def test_scaling_one_number(self):
        number = 35
        old_range = 0, 100
        new_range = 0, 1
        new = ForcedInvariance.scaling(None, number, old_range, new_range)
        self.assertEqual(new, 0.35)

    def test_scaling_array(self):
        array = np.array([[35, 35],
                          [35, 35]])
        old_range = 0, 100
        new_range = 0, 1
        check_array = np.array([[0.35, 0.35],
                                [0.35, 0.35]])
        new = ForcedInvariance.scaling(None, array, old_range, new_range)
        self.assertTrue(np.array_equal(new, check_array))


class StatisticsMethod(unittest.TestCase):
    def test_statistics_without_masks(self):
        band = np.array([[0, 0.39, 0.42],
                         [0.2, 0.4, 0.35]])
        index = np.array([[0.93, 0.24, 0.24],
                          [-0.35, 0.93, 0.24]])
        check_stat = {0.93:[0, 0.4],
                      0.24:[0.39, 0.42, 0.35],
                      -0.35:[0.2]}
        stat = ForcedInvariance.statistics(None, band, index)
        self.assertEqual(stat, check_stat)


class CorrelationMethod(unittest.TestCase):
    def test_correlation_method_basic(self):
        stat = {0.93:[0, 0.4],
                0.24:[0.39, 0.42, 0.35],
                -0.35:[0.2]}
        check_curve = {0.93:0.2, 0.24:0.39, -0.35:0.2}
        curve = ForcedInvariance.correlation(None, stat)
        for i in curve:
            curve[i] = round(curve[i], 2)
        self.assertEqual(curve, check_curve)


class SmoothingMethod(unittest.TestCase):
    def setUp(self):
        params = Parameters()
        self.fim = ForcedInvariance(params)

    def test_smoothing_with_one_window(self):
        curve = {0.96: 0.34, 0.51: 0.67, 0.52: 0.87, 0.11: 0.17, 0.18: 0.28}
        check_curve = {0.11: 0.17, 0.18: 0.28, 0.51: 0.67, 0.52: 0.87, 0.96: 0.34}
        self.fim.smoothing(curve)
        self.assertEqual(curve, check_curve)


class TargetValueMethod(unittest.TestCase):
    def setUp(self):
        params = Parameters()
        self.fim = ForcedInvariance(params)

    def test_target_value_by_mean_without_coefficient(self):
        band = np.array([[0.08366885, 0.33259951, 0.16066737, 0.18176515, 0.11411997],
                         [0.66369949, 0.09585974, 0.79209454, 0.83440211, 0.37460853],
                         [0.07946635, 0.5804281,  0.54472177, 0.98930503, 0.51080985]])
        check_target = 0.422547756751967
        target = self.fim.target_value(band)
        self.assertAlmostEqual(target, check_target)


class RecalculateMethod(unittest.TestCase):
    def setUp(self):
        params = Parameters()
        self.fim = ForcedInvariance(params)

    def test_recalculate_without_mask_and_scaling(self):
        band = np.array([[0.79667873, 0.05680854, 0.37823162, 0.76276089, 0.3857816],
        [0.14231934, 0.41198452, 0.38253771, 0.18997385, 0.57106195],
        [0.28108529, 0.92807336, 0.14973062, 0.78609907, 0.76275981]])
        index = np.array([[0.19958716, 0.47928994, 0.06913423, 0.12842111, 0.01005531],
        [0.62422291, 0.17398557, 0.01335282, 0.97057436, 0.57872553],
        [0.96914121, 0.803315,   0.29172871, 0.97018698, 0.15332311]])
        target = 0.4657257932012398
        curve = {0.19958716: 0.45194359033603027, 0.47928994: 0.0209933994420185, 0.06913423: 0.46648663805927537, 0.12842111: 0.5039957264445407, 0.01005531: 0.6950645360202986, 0.62422291: 0.5289273409105809, 0.17398557: 0.8603914602720266, 0.01335282: 0.2889846828956172, 0.97057436: 0.1292500940460929, 0.57872553: 0.43467328172539943, 0.96914121: 0.5355264612673543, 0.803315: 0.6322687670285159, 0.29172871: 0.142014264054789, 0.97018698: 0.15467813578386858, 0.15332311: 0.8533351250273246}
        check_band = np.array([[0.82097377, 1.26026285, 0.37761472, 0.70484213, 0.25849174],
        [0.12531359, 0.22300526, 0.61649523, 0.68453121, 0.61185789],
        [0.24444855, 0.68361387, 0.49103105, 2.36689311, 0.41629239]])
        self.fim.recalculate(band, curve, index, target, None)
        self.assertTrue(np.array_equal(np.around(band, 2), np.around(check_band, 2)))
