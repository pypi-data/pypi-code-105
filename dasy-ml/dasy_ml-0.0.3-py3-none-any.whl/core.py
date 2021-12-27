import numpy as np

class DataSynthesizer:
    """
    Samples input X data according to a specified process.
    """
    def __init__(self):
        pass

    def sample(self, n=100, dim=2):
        """
        Returns a sample of synthetic data. 
        @param n: Number of data points to sample
        @param dim: Dimension of data
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

