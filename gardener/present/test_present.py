class TestPresenter:
    def __init__(self, view):
        self.view = view

    def test_algorithm(self):
        result = 0.95
        self.view.showTestResult(result)

    def imagery_layer_choose(self, layer):
        self.__imagery_layer = layer

    def index_layer_choose(self, layer):
        self.__index_layer = layer

    def standard_layer_choose(self, layer):
        self.__standard_layer = layer

    def threshold_value_change(self, value):
        self.__threshold = value
