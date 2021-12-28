import numpy as np
from dasy.core import Labeler

class LinearRegressionLabeler(Labeler):
    """
    Label inputs x according to a linear function y=wx+b + e
    e is a noise term

    This is a probabilistic labeler, unless noise e=0. 
    """
    def __init__(self, dim=2, w=None, b=None, noise=np.random.normal):
        """
        @param dim
        @param w
        @param b
        @param noise: scalar function that takes a size argument, or None for no noise 
        """
        super().__init__()
        self.dim = dim
        if w is not None:
            self.w = w
        else:
            self.w = np.random.normal(size=dim)
        if b is not None:
            self.b = b
        else:
            self.b = 0
        if noise is not None:
            self.noise = noise
        else:
            self.noise = self.zero_function

    def assign(self, X):
        """
        @param X: matrix of inputs, where each row is an input vector x
        """
        # row-wise dot-product (w dot x for each x in X); add bias; add noise
        y = np.sum(self.w * X, axis=1) + self.b + self.noise(size=len(X)) #TODO: make it work for a single input?
        return y

    def zero_function():
        return 0
    



        
