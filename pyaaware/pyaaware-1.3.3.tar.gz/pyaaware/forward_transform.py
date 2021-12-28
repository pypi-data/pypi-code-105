import numpy as np


class ForwardTransform:
    def __init__(self,
                 N: (None, int) = None,
                 R: (None, int) = None,
                 bin_start: (None, int) = None,
                 bin_end: (None, int) = None,
                 ttype: (None, str) = None) -> None:
        import pyaaware

        self._ft = pyaaware._ForwardTransform()
        config = self._ft.config()

        if N is not None:
            config.N = N

        if R is not None:
            config.R = R

        if bin_start is not None:
            config.bin_start = bin_start

        if bin_end is not None:
            config.bin_end = bin_end

        if ttype is not None:
            config.ttype = ttype

        self._N = config.N
        self._R = config.R
        self._bins = config.bin_end - config.bin_start + 1
        self._ft.config(config, False)

    def execute(self, xt: np.ndarray) -> np.ndarray:
        assert (np.ndim(xt) == 2)

        samples = np.shape(xt)[0]
        channels = np.shape(xt)[1]

        frames = int(np.ceil(samples / self._R) + (self._N - self._R) / self._R)

        x = np.pad(xt, ((0, frames * self._R - samples), (0, 0)), 'constant')
        yf = np.zeros((self._bins, channels, frames), dtype=np.complex64)

        for channel in range(channels):
            for frame in range(frames):
                start = frame * self._R
                stop = start + self._R
                tmp = np.zeros(self._bins, dtype=np.complex64)
                self._ft.execute(x[start:stop, channel], tmp)
                yf[:, channel, frame] = tmp
            self._ft.reset()

        return yf

    def energy(self, x: np.ndarray) -> float:
        return self._ft.energy(x)
