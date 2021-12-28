import numpy as np


class SED:
    def __init__(self,
                 thresholds: None,
                 index: None,
                 frame_size: int = 64,
                 num_classes: int = 1,
                 mode: int = 0) -> None:
        import pyaaware

        self._num_classes = num_classes
        self._sed = pyaaware._SED()
        config = self._sed.config()

        config.frame_size = frame_size
        config.thresholds = [-38, -41, -48] if thresholds is None else thresholds
        config.num_classes = self._num_classes
        config.index = [1] if index is None else index
        config.mode = mode

        self._sed.config(config)

    def reset(self):
        self._sed.reset()

    def execute(self, x: np.ndarray) -> np.ndarray:
        y = np.zeros((self._num_classes, np.shape(x)[0]), dtype=np.float32)
        for in_idx in range(len(x)):
            y[:, in_idx] = self._sed.execute(x[in_idx])

        return y
