from abc import ABC, abstractmethod
from typing import Dict

from pynet.tensor import Tensor


class Loss(ABC):
    """Abstract class representing loss function."""

    def __init__(self) -> None:
        """Ctor."""
        super().__init__()

        self._stored_results = dict()

    @abstractmethod
    def forward(self, x: Tensor, y: Tensor) -> Dict[str, float]:
        """Performs forward step through the loss function.

        The <x> parameter represents neural network output, the <y> represents ground truth label 
        of the sample. If necessary, function can save intermediate results for the backward step 
        in the self._stored_results dictionary.
        
        Function should output all the possible measurable metrics, for the classification 
        problems these should be loss and accuracy, for the regression problem, only the loss 
        could be considered.

        Args:
            x (Tensor): Ouput (prediction) of the neural network.
            y (Tensor): Ground truth label.

        Returns:
            Dict[str, float]: All the possible measurable metrics for the loss function in format
                { name_of_metric_1: value_of_metric_1, ..., name_of_metric_n: value_of_metric_n }.
        """
        pass

    @abstractmethod
    def backward(self) -> Tensor:
        """Performs backward step through the loss function.

        Backward step is performed during the backpropagation procedure. As the loss function 
        is the last instance in the computational graph, it does not receive any intermediate 
        gradient tensor and should output derivative w.r.t. input <x> (i. e. neural network's 
        output) of the forward function.

        Returns:
            Tensor: Derivative w.r.t. input <x> (neural network's output) of the forward function.
        """
        pass
