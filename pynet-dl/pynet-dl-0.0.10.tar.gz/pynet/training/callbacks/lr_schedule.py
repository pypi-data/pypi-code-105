from typing import Callable

from pynet.optimizers.abstract import Optimizer
from pynet.training.callbacks.abstract import Callback
from pynet.training.history import History


class LrSchedule(Callback):
    """Callback providing functionality for scheduling the optimizer's learning rate."""

    def __init__(self, optimizer: Optimizer, schedule: Callable[[int, float], float]) -> None:
        """Ctor.

        Args:
            optimizer (Optimizer): Optimizer which learning rate will be scheduled.
            schedule (Callable[[int, float], float]): Learning rate scheduling function, 
                the function takes number of epoch and current learning rate as parameters 
                and outputs new learning rate based on these parameters.
        """
        super().__init__()

        self.__optimizer = optimizer
        self.__schedule = schedule

    def on_epoch_end(self, history: History) -> None:
        epoch = history.rows[-1].epoch
        lr = self.__optimizer.hyperparameters["lr"]
        new_lr = self.__schedule(epoch, lr)
        self.__optimizer.hyperparameters["lr"] = new_lr
