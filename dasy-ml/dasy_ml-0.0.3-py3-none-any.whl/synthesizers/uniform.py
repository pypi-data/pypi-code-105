import numpy as np
from dasy.core import DataSynthesizer

#TODO: switch from numpy random to Generator

class UniformSynth(DataSynthesizer):
    """
    Samples from a single Uniform Distribution on an interval
    """
    def sample(self, n=100, dim=2, low=-1., high=1.):
        return np.random.uniform(low=low, high=high, size=(n, dim))

