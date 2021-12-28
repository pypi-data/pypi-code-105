from abc import ABC, abstractmethod
from typing import List

from pynet.tensor import Tensor


class Optimizer(ABC):
    """Abstract class representing neural network's optimization algorithm.
    
    All the optimization algorithm's hyperparameters should be stored in self.hyperparameters
    dictionary.
    
    """

    def __init__(self) -> None:
        """Ctor."""
        super().__init__()

        self.hyperparameters = dict()

    @abstractmethod
    def register_parameters(self, params: List[Tensor]) -> None:
        """Registers neural network's parameters (weights) that will be optimized.

        Args:
            params (List[Tensor]): Neural network's parameters (weights) that will be optimized.
        """
        pass

    @abstractmethod
    def step(self) -> None:
        """Performs an optimization step.
        
        After the step, all registered parameters will be updated to the new value.
        
        """
        pass
