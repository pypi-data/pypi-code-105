import math
import numpy as np
from typing import Dict

from pynet.loss.abstract import Loss
from pynet.tensor import Tensor


class BinaryCrossEntropy(Loss):
    """Binary cross entropy implementation of the loss function. 
    
    Binary cross entropy is defined as: L(y, ŷ) = -(y * log(ŷ) + (1 - y) * log(1 - ŷ)) 
    where y is ground truth label and ŷ is neural network's prediction.
    """

    def __init__(self) -> None:
        """Ctor"""
        super().__init__()

    def forward(self, x: Tensor, y: Tensor) -> Dict[str, float]:
        assert all(
            [s == 1 for s in x.ndarray.shape]
        ), "BinaryCrossEntropy -> x input must be scalar"
        assert all(
            [s == 1 for s in y.ndarray.shape]
        ), "BinaryCrossEntropy -> y input must be scalar"

        x_scalar = np.squeeze(x.ndarray).item()
        y_scalar = np.squeeze(y.ndarray).item()

        # Add or subtract very small value to prevent math domain error
        # (i. e. taking the logarithm of zero).
        epsilon = 1e-8
        if x_scalar == 1.0:
            x_scalar -= epsilon
        if x_scalar == 0.0:
            x_scalar += epsilon

        self._stored_results["x"] = x_scalar
        self._stored_results["y"] = y_scalar
        self._stored_results["x_shape"] = x.ndarray.shape

        loss = -(y_scalar * math.log(x_scalar) + (1.0 - y_scalar) * math.log(1.0 - x_scalar))
        acc = 1 if round(x_scalar) == y_scalar else 0

        return {"loss": loss, "accuracy": acc}

    def backward(self) -> Tensor:
        x = self._stored_results["x"]
        y = self._stored_results["y"]
        shape = self._stored_results["x_shape"]

        dx = (x - y) / ((1.0 - x) * x)
        return Tensor(np.full(shape, dx))
