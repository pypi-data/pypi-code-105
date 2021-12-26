from pipoh.concrete_factories.bayesian_folder.bayesian_interface import InterfaceBayesian
import numpy as np


class BayesianEW(InterfaceBayesian):  # pylint: disable=too-few-public-methods
    """The EW Bayesian Concrete Class that implements the Bayesian interface"""

    def __init__(self, name='Equally Weighted Strategy', lamb=0, delta=0, upper_bound=0, lower_bound=0, validation_windows=0, cv_windows=0):
        self.name = name
        self.lamb = lamb
        self.delta = delta
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.validation_windows = validation_windows
        self.cv_windows = cv_windows
        self.data = []
        self.intermediate_data = []
        self.weights = []

    def get_dimensions(self):
        return {
            "Strategy Name": self.name,
            "Lambda initial value": self.lamb,
            "Beta initial value": self.delta
        }

    def get_all_parameters(self):
        return {
            "Strategy Name": self.name,
            "Lambda initial value": self.lamb,
            "Beta initial value": self.delta
        }

    def get_hyper_parameters(self):
        return "Hyper parameters selection done"

    def solve_optimization_problem(self):
        """
        Equally Weighted Strategy
        :param data_received:
        :param parameters:
        :param optimization:
        :return: It returns the optimized weights
        """
        name = 'Equally Weighted Strategy'

        (numElements, N) = self.data_received.shape
        # mean and covariance

        weights = np.ones((N, 1)) * (1 / N)
        self.weights = weights

        return self.weights


