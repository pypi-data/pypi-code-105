import numpy as np
from typing import List

from pynet.functional.abstract import Function
from pynet.tensor import Tensor


class Sigmoid(Function):
    """Function represents element-wise sigmoid function. 
    
    Sigmoid function is defined as S(x) = 1 / (1 + e^(-x)). Function takes one 
    tensor as input (i. e. len(x) == 1 in the forward method) and outputs an 
    tensor representing the sigmoid function result.
    """

    def __init__(self) -> None:
        """Ctor"""
        super().__init__()

    def forward(self, x: List[Tensor]) -> Tensor:
        assert len(x) == 1, "Sigmoid function takes 1 parameter"

        sig = 1.0 / (1.0 + np.exp(-x[0].ndarray))
        self._stored_results["sig"] = sig

        return Tensor(sig)

    def backward(self, y: Tensor) -> List[Tensor]:
        sig = self._stored_results["sig"]

        dsig = np.multiply(sig, 1.0 - sig)
        dsig = np.multiply(dsig, y.ndarray)

        return [Tensor(dsig)]
