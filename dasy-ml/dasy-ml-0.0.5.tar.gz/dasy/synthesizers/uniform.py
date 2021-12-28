import numpy as np
from dasy.core import DataSynthesizer

#TODO: switch from numpy random to Generator

class UniformSynth(DataSynthesizer):
    """
    Samples from a single Uniform Distribution on an interval
    """
    def __init__(self, dim, low=-10., high=10.):
        super().__init__(dim)
        self.low = low
        self.high = high

    def sample(self, n=100):
        return np.random.uniform(low=self.low, high=self.high, size=(n, self.dim))

