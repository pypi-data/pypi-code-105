from abc import ABCMeta, abstractmethod


class CommonBayesianFunctions(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_dimensions(self):
        return {
            "Strategy Name": self.name,
            "Lambda initial value": self.lamb,
            "Beta initial value": self.delta
        }

    @staticmethod
    @abstractmethod
    def get_all_parameters(self):
        return {
            "width": self._width,
            "depth": self._depth,
            "height": self._height
        }


def test_fcn(var1, var2):
    return var1+var2
