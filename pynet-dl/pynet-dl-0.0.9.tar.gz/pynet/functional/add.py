from typing import List

from pynet.functional.abstract import Function
from pynet.tensor import Tensor


class Add(Function):
    """Function represents addition operation between two tensors.

    Function takes two tensors as inputs (i. e. len(x) == 2 in the forward method) and outputs
    an tensor representing the addition operation result. Both inputs must have the same shape.
    """

    def __init__(self) -> None:
        """Ctor"""
        super().__init__()

    def forward(self, x: List[Tensor]) -> Tensor:
        shape1 = x[0].ndarray.shape
        shape2 = x[1].ndarray.shape

        assert len(x) == 2, "Add function takes 2 parameters"
        assert shape1 == shape2, f"Add -> Invalid input shapes: {shape1}, {shape2}"

        return Tensor(x[0].ndarray + x[1].ndarray)

    def backward(self, y: Tensor) -> List[Tensor]:
        return [Tensor(y.ndarray.copy()), Tensor(y.ndarray.copy())]
