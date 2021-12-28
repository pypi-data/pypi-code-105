from abc import ABC

from pynet.training.history import History


class Callback(ABC):
    """Abstract class representing callback object during the neural network training."""

    def __init__(self) -> None:
        """Ctor."""
        super().__init__()

    def on_epoch_begin(self) -> None:
        """Function called at the beginning of every training epoch."""
        pass

    def on_epoch_end(self, history: History) -> None:
        """Function called at the end of every training epoch.

        Args:
            history (History): History of the training.
        """
        pass

    def on_train_begin(self) -> None:
        """Function called at the beginning of the training."""
        pass

    def on_train_end(self, history: History) -> None:
        """Function called at the end of the training.

        Args:
            history (History): History of the training.
        """
        pass

    def on_test_begin(self) -> None:
        """Function called at the beginning of the testing."""
        pass

    def on_test_end(self, history: History) -> None:
        """Function called at the end of the testing.

        Args:
            history (History): History of the testing.
        """
        pass
