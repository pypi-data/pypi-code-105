from abc import ABC, abstractmethod

from pynet.tensor import Tensor


class Initializer(ABC):
    """Abstract class representing neural network's weights initializer."""

    def __init__(self) -> None:
        """Ctor"""
        super().__init__()

    @abstractmethod
    def initialize(self, inputs: int, outputs: int) -> Tensor:
        """Creates tensor of shape <outputs> x <inputs>.

        Elements of the tensor (i. e. weights) are initialized with values specific to the
        concrete implementation of the Initializer class.

        Args:
            inputs (int): Number of inputs to the layer to be initialized (columns of the weight matrix).
            outputs (int): Number of outputs of the layer to be initialized (rows of the weight matrix).

        Returns:
            Tensor: Initialized weight matrix.
        """
        pass
