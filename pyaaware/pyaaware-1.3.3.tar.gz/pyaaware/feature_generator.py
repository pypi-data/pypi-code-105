import numpy as np


class FeatureGenerator:
    def __init__(self,
                 frame_size: (None, int) = None,
                 feature_mode: (None, str) = None,
                 num_classes: (None, int) = None,
                 truth_mode: (None, int) = None,
                 bin_start: (None, int) = None,
                 bin_end: (None, int) = None) -> None:
        import pyaaware

        self._fg = pyaaware._FeatureGenerator()
        self._config = self._fg.config()

        if frame_size is not None:
            self._config.frame_size = frame_size

        if feature_mode is not None:
            self._config.feature_mode = feature_mode

        if num_classes is not None:
            self._config.num_classes = num_classes

        if truth_mode is not None:
            self._config.truth_mode = truth_mode

        if bin_start is not None:
            self._config.bin_start = bin_start

        if bin_end is not None:
            self._config.bin_end = bin_end

        self._bins = self._config.bin_end - self._config.bin_start + 1
        self._fg.config(self._config)

    @property
    def num_bands(self):
        return self._fg.num_bands()

    @property
    def stride(self):
        return self._fg.stride()

    @property
    def step(self):
        return self._fg.step()

    @property
    def decimation(self):
        return self._fg.decimation()

    @property
    def feature_size(self):
        return self._fg.feature_size()

    @property
    def feature_len(self):
        return self.num_bands * self.stride

    @property
    def num_classes(self):
        return self._config.num_classes

    @property
    def frame_size(self):
        return self._config.frame_size

    def execute(self, xf: np.ndarray, truth_in: (None, np.ndarray) = None) -> (np.ndarray, np.ndarray):
        assert (np.ndim(xf) == 3)
        bins = np.shape(xf)[0]
        channels = np.shape(xf)[1]
        input_frames = np.shape(xf)[2]

        assert (bins == self._bins)

        if truth_in is not None:
            assert (np.ndim(truth_in) == 3)
            assert (np.shape(truth_in)[0] == self.num_classes)
            assert (np.shape(truth_in)[1] == channels)
            assert (np.shape(truth_in)[2] == input_frames)

        output_frames = int(input_frames / (self.step * self.decimation))
        feature = np.zeros((self.feature_len, channels, output_frames))
        truth = np.zeros((self.num_classes, channels, output_frames))

        for channel in range(channels):
            output_frame = 0
            for input_frame in range(input_frames):
                if truth_in is not None:
                    self._fg.execute(xf[:, channel, input_frame], truth_in[:, channel, input_frame])
                else:
                    self._fg.execute(xf[:, channel, input_frame])

                if self._fg.eof():
                    feature[:, channel, output_frame] = self._fg.feature()
                    truth[:, channel, output_frame] = self._fg.truth()
                    output_frame += 1

        return feature, truth
