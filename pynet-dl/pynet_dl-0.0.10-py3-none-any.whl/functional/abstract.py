from abc import ABC, abstractmethod
from typing import List

from pynet.tensor import Tensor


class Function(ABC):
    """Abstract class representing any Tensor function."""

    def __init__(self) -> None:
        """Ctor"""
        super().__init__()

        self._stored_results = dict()

    @abstractmethod
    def forward(self, x: List[Tensor]) -> Tensor:
        """Performs forward step through the function.

        Function can have arbitrary number of operands, however, list <x> should be of the same 
        length as the number of operands this function takes. If necessary, function can save 
        intermediate results for the backward step in the self._stored_results dictionary.

        Args:
            x (List[Tensor]): Inputs (operands) to the function.

        Returns:
            Tensor: Function output.
        """
        pass

    @abstractmethod
    def backward(self, y: Tensor) -> List[Tensor]:
        """Performs backward step through the function.

        Backward step is performed during the backpropagation procedure. At the backward step, 
        the function receives gradient <y> and performs first derivation w.r.t. each of its 
        inputs <x> obtained during the forward step and returns these derivatives at the same 
        order as it received the inputs <x> during the forward step.

        Args:
            y (Tensor): Gradient from the consecutive function.

        Returns:
            List[Tensor]: List of first derivatives w.r.t. each of the function's inputs.
        """
        pass
