from .basic_transform import BasicTransform
from typing import List
import numpy as np


class Translation (BasicTransform):
    """
     Translates the image along the y-axis and colors the remaining part of the image with the chosen color.

     Parameters
     ----------
     shift_along_x : int
         Distance of the shift along x-axis.
     shift_along_y : int
         Distance of the shift along y-axis.
     color_value : int
         The chosen color for the remaining part of the image.
     """

    def __init__(self, shift_along_x, shift_along_y, color_value):
        self.shift_along_y = shift_along_y
        self.shift_along_x = shift_along_x
        self.color_value = color_value

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            height, width = im.shape[:2]
            if self.shift_along_y > height or self.shift_along_x > width:
                raise ValueError("shift_along_y and shift_along_x should be less then height and width of the image "
                                 "respectively")
            output_im = np.zeros(im.shape, dtype='u1')
            output_im[:] = self.color_value
            output_im[self.shift_along_y:, self.shift_along_x:] = im[:height - self.shift_along_y, :width-self.shift_along_x]
            res.append(output_im)
        return res


class TranslationX(BasicTransform):
    """
    Translates the image along the x-axis then adds a padding
    corresponding to the color value chosen.

     Parameters
     ----------
     shift_along_x : int
         Distance of the shift along x-axis.
     color_value : int
         The chosen color for the padding
    """

    def __init__(self, shift_along_x, color_value):
        self.shift_along_x = shift_along_x
        self.color_value = color_value

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            height, width = im.shape[:2]
            if self.shift_along_x > width:
                raise ValueError("shift_along_x should be less then width of the image")
            output_im = np.zeros(im.shape, dtype='u1')
            output_im[:] = self.color_value
            output_im[:, self.shift_along_x:] = im[:, :width - self.shift_along_x]
            res.append(output_im)
        return res


class TranslationY(BasicTransform):
    """
     Translates the image along the y-axis and colors the remaining part of the image with the chosen color.

     Parameters
     ----------
     shift_along_y : int
         Distance of the shift along y-axis.
     color_value : int
         The chosen color for the remaining part of the image.
     """

    def __init__(self, shift_along_y, color_value):
        self.shift_along_y = shift_along_y
        self.color_value = color_value

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            height, width = im.shape[:2]
            if self.shift_along_y > height:
                raise ValueError("shift_along_y should be less then height of the image")
            output_im = np.zeros(im.shape, dtype='u1')
            output_im[:] = self.color_value
            output_im[self.shift_along_y:, :] = im[:height - self.shift_along_y, :]
            res.append(output_im)
        return res
