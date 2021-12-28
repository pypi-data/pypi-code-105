from typing import Any, Tuple
import numpy as np
from pynet.data.abstract import Dataset


class InMemoryDataset(Dataset):
    """In-memory dataset implementation. 
    
    The class takes two numpy arrays x and y and provides basic iteration over the dataset
    and sample shuffling at the end of the iteration as well.
    """

    def __init__(self, x: np.ndarray, y: np.ndarray) -> None:
        """Ctor

        Args:
            x (np.ndarray): Dataset samples.
            y (np.ndarray): Corresponding labels for samples.
        """
        super().__init__()

        assert len(x) == len(y), "x and y must have same length"

        self.__x = x
        self.__y = y

    def __len__(self) -> int:
        return len(self.__x)

    def __getitem__(self, idx) -> Tuple[Any, Any]:
        xi = self.__x[idx]
        yi = self.__y[idx]

        return xi, yi

    def reset(self) -> None:
        super().reset()

        p = np.random.permutation(len(self.__x))
        self.__x, self.__y = self.__x[p], self.__y[p]
