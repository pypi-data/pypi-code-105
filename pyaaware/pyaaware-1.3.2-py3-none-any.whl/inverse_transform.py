import numpy as np


class InverseTransform:
    def __init__(self,
                 N: (None, int) = None,
                 R: (None, int) = None,
                 bin_start: (None, int) = None,
                 bin_end: (None, int) = None,
                 ttype: (None, str) = None,
                 gain: (None, float) = None) -> None:
        import pyaaware

        self._it = pyaaware._InverseTransform()
        config = self._it.config()

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

        if gain is not None:
            config.gain = gain

        self._N = config.N
        self._R = config.R
        self._bins = config.bin_end - config.bin_start + 1
        self._it.config(config, False)

    def execute(self, xf: np.ndarray) -> np.ndarray:
        assert (np.ndim(xf) == 3)

        bins = np.shape(xf)[0]
        channels = np.shape(xf)[1]
        frames = np.shape(xf)[2]

        assert (bins == self._bins)

        samples = frames * self._R

        yt = np.zeros((samples, channels), dtype=np.float32)

        for channel in range(channels):
            for frame in range(frames):
                start = frame * self._R
                stop = start + self._R
                tmp = np.zeros(self._R, dtype=np.float32)
                self._it.execute(xf[:, channel, frame], tmp)
                yt[start:stop, channel] = tmp
            self._it.reset()

        return yt
