"""A Class of Strategy"""

"""
from pyGPGO.covfunc import squaredExponential
from pyGPGO.acquisition import Acquisition
from pyGPGO.surrogates.GaussianProcess import GaussianProcess
from pyGPGO.GPGO import GPGO
"""
import numpy as np

from pipoh.concrete_factories.bayesian_folder.bayesian_interface import InterfaceBayesian
from pipoh.concrete_factories.bayesian_folder.bayesian_strategies.bayesian_common_functions import test_fcn
from sklearn.covariance import EmpiricalCovariance
from qpsolvers import solve_qp


class BayesianWUBC(InterfaceBayesian):

    def __init__(self, name='Weighted Upper Bound Constraint, WUBC', lamb=1, delta=1, upper_bound=1, lower_bound=0, validation_windows=36, cv_windows=12):
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
        self.optim_param = {}

    def get_dimensions(self):
        return {
            "Strategy Name": self.name,
            "Lambda initial value": self.lamb,
            "Upper bound limit initial value": self.upper_bound
        }

    def get_all_parameters(self):
        return {
            "Strategy Name": self.name,
            "Lambda initial value": self.lamb,
            "Upper bound limit initial value": self.upper_bound,
            "CV windows": self.cv_windows
        }

    def get_hyper_parameters(self):

        return test_fcn(self.lamb, self.delta)


    def solve_optimization_problem(self):
        # Type: It returns the optimized weights
        # Compute numbers of data points and assets
        #lambdaValue=self.optim_param.get('lambda_value')
        (numElements, N) = self.intermediate_data.shape
        # mean and covariance
        assert np.count_nonzero(np.isnan(self.intermediate_data)) == 0
        if len(self.intermediate_data)==0:
            pass
        try:
            Sigma = EmpiricalCovariance().fit(self.intermediate_data).covariance_ * 12  # I use 12 for annualizing the covmatrix
        except:
            pass
        Vars = np.diag(Sigma)  # variances of the stocks
        mu = self.intermediate_data.mean(axis=0).H * 12  # mean log returns

        lambdaValue = self.lamb
        # lambdaValue = 0.886
        upperBoundValue = self.upper_bound
        # lowerBoundValue = 0
        H = 2 * (lambdaValue * Sigma)
        f = - mu.H  # FALTA TRANSPOSE

        Aeq = np.ones((1, N))
        beq = 1
        LB = np.ones((1, N))
        UB = np.ones((1, N)) * upperBoundValue

        P = H
        q = np.asarray(f).reshape((6,))
        G = np.zeros((6, 6))
        h = np.zeros(6)
        A = np.asarray(Aeq).reshape((6,))
        b = np.array([beq])
        lb = LB
        ub = UB

        # (Wa, varP, third_parameter) = solve_qp(P, q, G, h, A, b)
        W = np.array(solve_qp(P, q, G, h, A, b))
        #W = np.ones((6, 1))

        return W
