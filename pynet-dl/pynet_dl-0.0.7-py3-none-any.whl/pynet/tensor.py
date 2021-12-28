import numpy as np


class Tensor:
    """Represents n-dimensional array (tensor)."""

    def __init__(self, ndarray: np.ndarray) -> None:
        """Ctor.

        Args:
            ndarray (np.ndarray): Elements of the tensor.
        """
        self.ndarray = ndarray
        self.grad = None
