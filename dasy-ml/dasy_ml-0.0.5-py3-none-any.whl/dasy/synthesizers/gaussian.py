import numpy as np
from dasy.core import DataSynthesizer

#TODO: switch from numpy random to Generator

class GaussianSynth(DataSynthesizer):
    """
    Samples from a single multivariate Normal Distribution
    """
    def __init__(self, dim=None, mean=None, cov=None):
        """
        @param dim: input dimension 
        @param mean: dim-dimensional point
        @param cov: dim x dim covariance matrix
        """
        super().__init__(dim)
        self.mean = mean
        self.cov = cov
        # set defaults
        if mean is None:
            self.mean = np.zeros(dim)
        if cov is None:
            self.cov = np.eye(dim)
        if len(self.mean) != dim:
            raise ValueError(f'mean must have dimension = {dim} (is {len(self.mean)})')
        if len(self.cov) != dim:
            raise ValueError(f'cov must have dimension = {dim} x {dim} (is {self.cov.shape[0]} x {self.cov.shape[1]})')

    def sample(self, n=100):
        """
        See numpy.random.multivariate_normal for details on params
        We add simple defaults for mean and cov
        """
        return np.random.multivariate_normal(mean=self.mean, cov=self.cov, size=n)

