from typing import List

import pynet.functional.sigmoid
from pynet.nn.abstract import Module
from pynet.tensor import Tensor


class Sigmoid(Module):
    """Module representing sigmoid activation function.

    Applies the sigmoid function element-wise, sigmoid function is defined as:
    S(x) = 1 / (1 + e^(-x)), where x is module's input.
    """

    def __init__(self) -> None:
        """Ctor."""
        super().__init__()

        self.__sigmoid = pynet.functional.sigmoid.Sigmoid()

    def forward(self, x: Tensor) -> Tensor:
        y = self.__sigmoid.forward([x])
        return y

    def backward(self, y: Tensor) -> Tensor:
        dx = self.__sigmoid.backward(y)[0]
        return dx

    def get_parameters(self) -> List[Tensor]:
        return []
