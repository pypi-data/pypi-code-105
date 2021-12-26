import numpy as np

from abc import ABCMeta, abstractmethod, ABC

class fnc_EW(ABC):
    __metaclass__=ABCMeta
    @abstractmethod
    def solve_optimization_problem(self):
        """
        Equally Weighted Strategy
        :param data_received:
        :param parameters:
        :param optimization:
        :return: It returns the optimized weights
        """
        name = 'Equally Weighted Strategy'

        (numElements, N) = self.intermediate_data.shape
        # mean and covariance

        weights = np.ones((N, 1)) * (1 / N)
        self.weights = weights

        return self.weights
