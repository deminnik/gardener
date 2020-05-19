import unittest

from gardener.model.unveiling import Parameters


class SetScalesMethod(unittest.TestCase):
    def setUp(self):
        self.parameters = Parameters()
    
    def test_set_none_scales(self):
        self.parameters.scales = None
        self.assertIsNone(self.parameters.scales)

    def test_set_some_scales(self):
        scales = 1, 5
        self.parameters.scales = scales
        self.assertEqual(self.parameters.scales, scales)


class SetBinsMethod(unittest.TestCase):
    def setUp(self):
        self.parameters = Parameters()
    
    def test_set_none_bins(self):
        self.parameters.bins = None
        self.assertIsNone(self.parameters.bins)

    def test_set_some_bins(self):
        bins = 3, 3
        self.parameters.bins = bins
        self.assertEqual(self.parameters.bins, bins)


class SetThresholdsMethod(unittest.TestCase):
    def setUp(self):
        self.parameters = Parameters()
    
    def test_set_none_thresholds(self):
        self.parameters.thresholds = None
        self.assertIsNone(self.parameters.thresholds)

    def test_set_some_thresholds(self):
        thresholds = 0.2, 0.8
        self.parameters.thresholds = thresholds
        self.assertEqual(self.parameters.thresholds, thresholds)


class SetWindowsMethod(unittest.TestCase):
    def setUp(self):
        self.parameters = Parameters()

    def test_set_some_windows(self):
        windows = 3, 5, 7
        self.parameters.windows = windows
        self.assertEqual(self.parameters.windows, windows)

    def test_count_of_set_windows(self):
        windows = 3, 5, 7
        self.parameters.windows = windows
        self.assertEqual(len(self.parameters.windows), len(windows))


class SetCoefficientMethod(unittest.TestCase):
    def setUp(self):
        self.parameters = Parameters()

    def test_set_some_coefficient(self):
        coefficient = 1.5
        self.parameters.coefficient = coefficient
        self.assertEqual(self.parameters.coefficient, coefficient)


class SetMaskMethod(unittest.TestCase):
    def setUp(self):
        self.parameters = Parameters()
    
    def test_set_none_mask(self):
        self.parameters.mask = None
        self.assertIsNone(self.parameters.mask)
