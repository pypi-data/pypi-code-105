from pipoh.concrete_factories.non_parametric.non_parametric_interface import InterfaceNonParametric
from pipoh.common_functions.rolling_windows_validation import rolling_windows_validation
from pipoh.strategies.class_ew import fnc_EW


class EW(fnc_EW, InterfaceNonParametric):
    def __init__(self, name='Equally Weighted Strategy', lamb=0, delta=0, upper_bound=0, lower_bound=0, validation_windows=36, cv_windows=12):
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
        self.returns = []

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
        return rolling_windows_validation(self.data)


    def solve_optimization_problem(self):
        return super().solve_optimization_problem()

