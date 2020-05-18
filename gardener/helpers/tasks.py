from qgis.core import QgsTask

from gardener.model.unveiling import Raster


class FImTask(QgsTask):
    def __init__(self, image_name, index_name):
        title = "Unveiling by FIM"
        layers = f"image('{image_name}'), index('{index_name}')"
        name = f"{title}: {layers}"
        super().__init__(name, QgsTask.CanCancel)

    def configure(self, algorithm, argument):
        self.__fim = algorithm
        self.__img = argument
    
    def run(self):
        try:
            self.__fim(self.__img)
        except:
            return False
        else:
            del self.__img
            return True


class PlotTask(QgsTask):
    def __init__(self, image_name, band_name, index_name):
        title = "Statistics by FIM"
        layers = f"image('{image_name}', band('{band_name}')), index('{index_name}')"
        name = f"{title}: {layers}"
        super().__init__(name, QgsTask.CanCancel)

    def presenter(self, presenter):
        self.__presenter = presenter

    def configure(self, algorithm, band, imagery):
        self.__fim = algorithm
        self.__band = band
        self.__img = imagery
    
    def run(self):
        try:
            self.__curve, self.__cloud = self.__fim(self.__band-1, self.__img)
        except Exception as e:
            raise e
        else:
            return True

    def finished(self, result):
        if result:
            frame = self.__presenter.view.PlotFrame(self.__curve, self.__cloud)
            self.__presenter.displaying_finished(self.__band, frame)

    def cancel(self):
        self.__presenter.displaying_error()
        super().cancel()


class TestTask(QgsTask):
    def __init__(self, image_name, model_name):
        title = "Evaluating"
        layers = f"image('{image_name}'), standard('{model_name}')"
        name = f"{title}: {layers}"
        super().__init__(name, QgsTask.CanCancel)

    def presenter(self, presenter):
        self.__presenter = presenter

    def configure(self, comparator, fim, imagery, standard, temp):
        self.__comparator = comparator
        self.__fim = fim
        self.__imagery = imagery
        self.__standard = standard
        self.__unveiled = temp
    
    def run(self):
        try:
            self.__fim(self.__imagery)
            result = Raster(self.__unveiled)
            self.__similarity = self.__comparator(result.raster, 
                                                    self.__standard.raster)
        except Exception as e:
            raise e
        else:
            return True

    def finished(self, result):
        if result:
            self.__presenter.testing_finished(self.__similarity)

    def cancel(self):
        self.__presenter.testing_error()
        super().cancel()
