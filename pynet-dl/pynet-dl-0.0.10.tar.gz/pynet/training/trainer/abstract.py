from abc import ABC, abstractmethod
from typing import List

from pynet.nn.abstract import Module
from pynet.data.abstract import Dataset
from pynet.loss.abstract import Loss
from pynet.optimizers.abstract import Optimizer
from pynet.training.callbacks.abstract import Callback
from pynet.training.history import History


class Trainer(ABC):
    """Abstract class providing neural network's training/testing procedure."""

    def __init__(self) -> None:
        """Ctor."""
        super().__init__()

    @abstractmethod
    def train(
        self,
        model: Module,
        train_dataset: Dataset,
        val_dataset: Dataset,
        loss_f: Loss,
        optimizer: Optimizer,
        epochs: int,
        callbacks: List[Callback] = [],
    ) -> History:
        """Function performing training procedure of the neural network.

        Args:
            model (Module): Neural network to be trained.
            train_dataset (Dataset): Dataset that will be used for network's training.
            val_dataset (Dataset): Dataset that will be used for network's validation (can be None).
            loss_f (Loss): Neural network's loss function.
            optimizer (Optimizer): Optimizer that will be used for network's optimization.
            epochs (int): Number of training epochs.
            callbacks (List[Callback], optional): List of callbacks called during the training. Defaults to [].

        Returns:
            History: Neural network's training history.
        """
        pass

    @abstractmethod
    def test(
        self, model: Module, test_dataset: Dataset, loss_f: Loss, callbacks: List[Callback] = []
    ) -> History:
        """Function performing testing procedure of the neural network.

        Args:
            model (Module): Neural network to be tested.
            test_dataset (Dataset): Dataset that will be used for network's testing.
            loss_f (Loss): Neural network's loss function.
            callbacks (List[Callback], optional): List of callbacks called during the testing. Defaults to [].

        Returns:
            History: Neural network's testing history.
        """
        pass
