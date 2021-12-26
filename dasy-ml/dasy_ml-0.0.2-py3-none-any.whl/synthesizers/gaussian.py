import numpy as np
from dasy.core import DataSynthesizer

#TODO: switch from numpy random to Generator

class GaussianSynth(DataSynthesizer):
    """
    Samples from a single multivariate Normal Distribution
    """
    def sample(self, n=100, dim=2, mean=None, cov=None):
        """
        See numpy.random.multivariate_normal for details on params
        We add simple defaults for mean and cov
        """
        if mean is None:
            mean = np.zeros(dim)
        if cov is None:
            cov = np.eye(dim)
        return np.random.multivariate_normal(mean=mean, cov=cov, size=n)

