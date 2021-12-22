from abc import ABC, abstractmethod
import numpy as np


class BasicTransform(ABC):
    @staticmethod
    def check_images(images):
        for im in images:
            if not (isinstance(im, np.ndarray)):
                raise TypeError

    @abstractmethod
    def transform(self, images):
        pass
