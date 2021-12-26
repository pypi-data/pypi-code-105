import numpy as np
from sklearn.covariance import EmpiricalCovariance
from qpsolvers import solve_qp

from abc import ABCMeta, abstractmethod, ABC

class fnc_WLBC(ABC):
    __metaclass__ = ABCMeta
    def __init__(self, name='Weighted lower Bound Constraint, WUBC', lamb=1, delta=1, upper_bound=1, lower_bound=0, validation_windows=36, cv_windows=12) -> None:
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

    @abstractmethod
    def solve_optimization_problem(self):
        # Type: It returns the optimized weights
        # Compute numbers of data points and assets
        lambdaValue=self.optim_param.get('lambda_value')
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
        lowerBoundValue = self.lower_bound
        # lowerBoundValue = 0
        H = 2 * (lambdaValue * Sigma)
        f = - mu.H  # FALTA TRANSPOSE

        Aeq = np.ones((1, N))
        beq = 1
        LB = np.ones((1, N))* lowerBoundValue
        UB = np.ones((1, N))

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
