import numpy as np

class DataSynthesizer:
    """
    Samples input X data according to a specified process.
    """
    def __init__(self, dim):
        """
        @param dim: Dimension of data
        """
        self.dim = dim

    def sample(self, n=100):
        """
        Returns a sample of synthetic data. 
        @param n: Number of data points to sample
        @return data X
        """
        raise NotImplementedError

class Labeler:
    """
    Assigns labels y to input X data. 
    """
    def __init__(self, classes=0):
        self.classes = classes

    def assign(self, X):
        """
        Assign labels y to input X data
        @return labels y, aligned with X
        """
        raise NotImplementedError

#TODO: should we have separate classes for RegressionLabeler and ClassificationLabeler? (current hack is use classes=0 for RegressionLabeler)
