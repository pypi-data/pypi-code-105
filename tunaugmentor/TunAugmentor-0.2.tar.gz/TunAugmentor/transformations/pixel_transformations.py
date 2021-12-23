from .basic_transform import BasicTransform
from typing import List
import numpy as np


class ChangeBrightness(BasicTransform):
    """
     Adds Brightness to the image

     Parameters
     ----------
     brightness_value : int
         Brightness value to add. Positive to lighten the image and negative to darken the image
     """

    def __init__(self, brightness_value):
        self.brightness_value = brightness_value

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            tmp = np.ones(im.shape) * self.brightness_value
            res.append(np.add(im, tmp))
        return res


class AddGaussianNoise(BasicTransform):
    """
     Adds gaussian noise to the image

     Parameters
     ----------
     mean : float
         mean of the noise
     var : float
         variance of the noise
     """

    def __init__(self, mean, var):
        self.mean = mean
        self.var = var
        self.sigma = var ** 0.5

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            noise = np.random.normal(self.mean, self.sigma, im.shape)
            res.append(np.add(noise, im))
        return res


class ColorModification(BasicTransform):
    """
     Modifies the colors on each channel.

     Parameters
     ----------
     red_shift : int
         shift on the red channel
     green_shift : int
         shift on the green channel
     blue_shift : int
         shift on the blue channel
     """

    def __init__(self, red_shift, green_shift, blue_shift):
        self.red_shift = red_shift
        self.green_shift = green_shift
        self.blue_shift = blue_shift

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            tmp = im.copy()
            tmp[:, :, 0] = tmp[:, :, 0] + self.red_shift
            tmp[:, :, 1] = tmp[:, :, 1] + self.green_shift
            tmp[:, :, 2] = tmp[:, :, 2] + self.blue_shift
            res.append(tmp)
        return res
