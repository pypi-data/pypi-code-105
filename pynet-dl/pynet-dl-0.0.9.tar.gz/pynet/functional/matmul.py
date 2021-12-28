import numpy as np
from typing import List

from pynet.functional.abstract import Function
from pynet.tensor import Tensor


class Matmul(Function):
    """Function represents matrix multiplication.

    Function takes two tensors as inputs (i. e. len(x) == 2 in the forward method) 
    and outputs an tensor representing the matrix multiplication operation result. 
    At the current version, this operation supports only tensors with dimensions <= 2. 
    
    If x[0] is an m × n matrix and x[1] is an n × p matrix, the result is defined to be
    the m × p matrix.
    """

    def __init__(self) -> None:
        """Ctor"""
        super().__init__()

    def forward(self, x: List[Tensor]) -> Tensor:
        assert len(x) == 2, "Matmul function takes 2 parameters"
        assert (
            x[0].ndarray.ndim <= 2 and x[1].ndarray.ndim <= 2
        ), "Forward -> Matrix multiplication of tensors with dimensions > 2 are not supported, yet"

        y = np.matmul(x[0].ndarray, x[1].ndarray)

        self._stored_results["a"] = x[0]
        self._stored_results["b"] = x[1]

        return Tensor(y)

    def backward(self, y: Tensor) -> List[Tensor]:
        assert (
            y.ndarray.ndim <= 2
        ), "Backward -> Matrix multiplication of tensors with dimensions > 2 are not supported, yet"

        a = self._stored_results["a"]
        b = self._stored_results["b"]

        da = np.matmul(y.ndarray, b.ndarray.T)
        db = np.matmul(a.ndarray.T, y.ndarray)

        return [Tensor(da), Tensor(db)]
