import numpy as np
from typing import List

from pynet.functional.max import Max
from pynet.nn.abstract import Module
from pynet.tensor import Tensor


class ReLU(Module):
    """Module representing ReLU activation function.

    Applies the rectified linear unit (ReLU) function element-wise, ReLU function is defined as:
    ReLU(x) = max(0, x), where x is module's input.
    """

    def __init__(self) -> None:
        """Ctor."""
        super().__init__()

        self.__max = Max()

    def forward(self, x: Tensor) -> Tensor:
        zeros = Tensor(np.zeros_like(x.ndarray))
        y = self.__max.forward([x, zeros])
        return y

    def backward(self, y: Tensor) -> Tensor:
        dx, dzeros = self.__max.backward(y)
        return dx

    def get_parameters(self) -> List[Tensor]:
        return []
