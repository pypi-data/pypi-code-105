from typing import List

from pynet.training.stats import Statistics


class HistoryRow:
    """Represents single history's record (row)."""

    def __init__(self, epoch: int, stats: List[Statistics]) -> None:
        """Ctor.

        Args:
            epoch (int): Number of epoch.
            stats (List[Statistics]): All the measured metrics within the epoch.
        """
        self.epoch = epoch
        self.stats = stats


class History:
    """Class holding all the measured metrics of the model during the model's training/testing."""

    def __init__(self) -> None:
        """Ctor."""
        self.rows = []

    def add(self, epoch: int, stats: List[Statistics]) -> None:
        """Adds new record to the history.

        Args:
            epoch (int): Number of epoch.
            stats (List[Statistics]): All the measured metrics within the epoch.
        """
        self.rows.append(HistoryRow(epoch, stats))
