import numpy as np

from pynet.initializers.abstract import Initializer
from pynet.tensor import Tensor


class HeNormal(Initializer):
    """Initializes weight matrix by He normal initialization. 
    
    He normal initialization is defined as: W = N(0, 1) * sqrt(2 / <inputs>), where N(0, 1) denotes 
    standard normal distribution and <inputs> represents number of inputs to the layer (i. e. 
    number of weight matrix columns). For more information, see: https://arxiv.org/abs/1502.01852.
    """

    def __init__(self) -> None:
        """Ctor"""
        super().__init__()

    def initialize(self, inputs: int, outputs: int) -> Tensor:
        ndarray = np.random.randn(outputs, inputs) * np.sqrt(2.0 / (inputs))
        return Tensor(ndarray)
