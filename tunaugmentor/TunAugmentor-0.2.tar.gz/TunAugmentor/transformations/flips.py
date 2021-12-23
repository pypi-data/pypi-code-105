from .basic_transform import BasicTransform
from typing import List
import numpy as np


class Flip(BasicTransform):
    """
     Flips the image horizontally, vertically or both.

     Parameters
     ----------
     v : bool
         True to flip vertically, else False. Default False
     h : bool
         True to flip horizontally, else False. Default False
     """
    def __init__(self, v=False, h=False):

        self.v = -1 if v else 1
        self.h = -1 if h else 1

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            res.append(im[::self.v, ::self.h, :])
        return res


class FlipVertical(BasicTransform):
    """
    Flips the image vertically.
    """
    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            res.append(im[::-1, :, :])
        return res


class FlipHorizontal(BasicTransform):
    """
    Flips the image horizontally
    """
    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            res.append(im[:, ::-1, :])
        return res


