from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Tuple


class Dataset(ABC):
    """Abstract class providing basic functionality for dataset manipulation.

    Provides basic functionality such as iteration over the dataset.
    Derived classes must implement __len__ and __getitem__ methods.
    """

    def __init__(self) -> None:
        """Ctor"""
        super().__init__()

        self.__idx = -1

    @abstractmethod
    def __len__(self) -> int:
        """Returns number of samples in the dataset.

        Returns:
            int: Number of samples in the dataset.
        """
        pass

    @abstractmethod
    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        """Returns i-th item from the dataset. 
        
        Return value should be a tuple of sample x and its corresponding label y (xi, yi).

        Args:
            idx (int): Index of sample that should be returned.

        Returns:
            Tuple[Any, Any]: Tuple of sample x and its corresponding label y (xi, yi).
        """
        pass

    def __iter__(self) -> Dataset:
        """Returns iterator over the Dataset

        Returns:
            Dataset: The dataset.
        """
        return self

    def __next__(self) -> Tuple[Any, Any]:
        """Moves an iterator to the next sample

        Raises:
            StopIteration: Signals the end of the iteration.

        Returns:
            Tuple[Any, Any]: Tuple of sample x and its corresponding label y (xi, yi).
        """
        self.__idx += 1

        if self.__idx < len(self):
            return self.__getitem__(self.__idx)

        self.reset()
        raise StopIteration

    def reset(self) -> None:
        """Resets the iterator to the initial state"""
        self.__idx = -1
