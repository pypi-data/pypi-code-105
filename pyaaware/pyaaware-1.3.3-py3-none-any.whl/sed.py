import numpy as np


class SED:
    def __init__(self,
                 thresholds: (None, list) = None,
                 index: (None, list) = None,
                 frame_size: (None, int) = None,
                 num_classes: (None, int) = None,
                 mode: (None, int) = None) -> None:
        import pyaaware

        self._sed = pyaaware._SED()
        config = self._sed.config()

        if thresholds is not None:
            config.thresholds = thresholds

        if index is not None:
            config.index = index

        if frame_size is not None:
            config.frame_size = frame_size

        if num_classes is not None:
            config.num_classes = num_classes

        if mode is not None:
            config.mode = mode

        self._num_classes = config.num_classes
        self._sed.config(config)

    def reset(self):
        self._sed.reset()

    def execute(self, x: np.ndarray) -> np.ndarray:
        y = np.zeros((self._num_classes, np.shape(x)[0]), dtype=np.float32)
        for in_idx in range(len(x)):
            y[:, in_idx] = self._sed.execute(x[in_idx])

        return y
