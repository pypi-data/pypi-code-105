import numpy as np
from typing import List

from pynet.functional.abstract import Function
from pynet.tensor import Tensor


class Max(Function):
    """Function represents element-wise maximum function between two tensors.

    Function takes two tensors as inputs (i. e. len(x) == 2 in the forward method) and outputs
    an tensor representing the maximum operation result. Both inputs must have the same shape.
    """

    def __init__(self) -> None:
        """Ctor"""
        super().__init__()

    def forward(self, x: List[Tensor]) -> Tensor:
        shape1 = x[0].ndarray.shape
        shape2 = x[1].ndarray.shape

        assert len(x) == 2, "Max function takes 2 parameters"
        assert shape1 == shape2, f"Max -> Invalid input shapes: {shape1}, {shape2}"

        self._stored_results["mask_a"] = x[0].ndarray > x[1].ndarray
        self._stored_results["mask_b"] = x[1].ndarray > x[0].ndarray

        y = np.maximum(x[0].ndarray, x[1].ndarray)
        return Tensor(y)

    def backward(self, y: Tensor) -> List[Tensor]:
        mask_a = self._stored_results["mask_a"]
        mask_b = self._stored_results["mask_b"]

        da = np.multiply(y.ndarray, mask_a)
        db = np.multiply(y.ndarray, mask_b)

        return [Tensor(da), Tensor(db)]
