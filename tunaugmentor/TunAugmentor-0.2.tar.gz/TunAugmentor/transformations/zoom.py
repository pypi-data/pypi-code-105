from .basic_transform import BasicTransform
from typing import List
import numpy as np


class CenterZoom(BasicTransform):
    """
     Zooms in the center of an image.

     Parameters
     ----------
     zoom_factor : int
         the factor to zoom with.
     """

    def __init__(self, zoom_factor):
        self.zoom_factor = zoom_factor
        if not isinstance(zoom_factor, int):
            raise ValueError("zoom_factor should be int")

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []

        for im in images:
            x, y = im.shape[:2]
            tmp = im.repeat(self.zoom_factor, axis=0).repeat(self.zoom_factor, axis=1)
            x_center = tmp.shape[0] // 2
            y_center = tmp.shape[1] // 2
            res.append(tmp[x_center - x // 2:x_center + x // 2,
                       y_center - y // 2:y_center + y // 2])
        return res
