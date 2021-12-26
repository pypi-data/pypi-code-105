from collections import deque
from typing import Any, List, Union

import numpy as np

from supply_depot.rl.replay import BaseReplayBuffer


class ReplayBuffer(BaseReplayBuffer):
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.buffer = deque(maxlen=max_size)

    def __getitem__(self, idx: Union[int, List[int]]) -> Any:
        if isinstance(idx, int):
            return self.buffer[idx]
        return [self.buffer[i] for i in idx]

    def __setitem__(self, idx: Union[int, List[int]], data: Any) -> Any:
        if isinstance(idx, int):
            self.buffer[idx] = data
        else:
            for i in range(len(idx)):
                self.buffer[idx[i]] = data[i]

    def sample(self, num_samples: int, replace: bool = False) -> List[Any]:
        buffer_len = len(self.buffer)
        sampled_indices = np.random.choice(
            np.arange(buffer_len), num_samples, replace=replace
        )
        return [self.buffer[i] for i in sampled_indices]

    def append(self, sample: Any) -> None:
        self.buffer.append(sample)

    def remove(self, idx: int) -> None:
        del self.buffer[idx]
