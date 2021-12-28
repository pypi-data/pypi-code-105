from abc import ABC, abstractmethod
from typing import List

from pynet.tensor import Tensor


class Module(ABC):
    """Abstract class representing neural network's module."""

    def __init__(self) -> None:
        """Ctor."""
        super().__init__()

    @abstractmethod
    def forward(self, x: Tensor) -> Tensor:
        """Performs forward step through the module.

        During the forward step, module performs all the operations with the input tensor <x> 
        correspondig to the module and returns tensor representing an output of the module. 
        For the operations, it should use some of the Function abstract class implementations. 
        If needed, new Function implementation can be created.

        Args:
            x (Tensor): Input tensor to the module.

        Returns:
            Tensor: Module's output tensor.
        """
        pass

    @abstractmethod
    def backward(self, y: Tensor) -> Tensor:
        """Performs backward step through the module.

        Backward step is performed during the backpropagation procedure. At the backward step, 
        the module receives gradient <y> and performs backward steps for each of the operations
        performed during the forward step in reverse order and sets <grad> property of each of 
        the module's parameters (weights) to the derivative w.r.t. to that parameter. Finally, 
        returns derivative w.r.t. tensor <x> obtained in the forward step.

        Args:
            y (Tensor): Gradient from the consecutive module/function.

        Returns:
            Tensor: Derivative (gradient) w.r.t. tensor <x> obtained in the forward step.
        """
        pass

    @abstractmethod
    def get_parameters(self) -> List[Tensor]:
        """Returns all the module's parameters (trainable weights).

        Returns:
            List[Tensor]: List of module's parameters (trainable weights).
        """
        pass
