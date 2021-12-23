from .basic_transform import BasicTransform
from typing import List
import numpy as np
import random


class Crop(BasicTransform):
    """
     Crops the area of the image limited by xmin,xmax and ymin,ymax.

     Parameters
     ----------
     xmin : int
         minimum x coordinate.
     xmax : int
         maximum x coordinate.
     ymin : int
         minimum y coordinate.
     ymax : int
         maximum y coordinate.
     """

    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            x, y = im.shape[:2]
            if self.xmin < 0 or self.xmax < self.xmin:
                raise ValueError("xmin,xmax should be positive and xmax>xmin")
            if self.ymin < 0 or self.ymax < self.ymin:
                raise ValueError("ymin,ymax should be positive and ymax>ymin")
            if x < self.xmax or y < self.ymax:
                raise ValueError("We should have xmax<X and ymax<Y")
            res.append(im[self.xmin:self.xmax, self.ymin:self.ymax, :])
        return res


class CenterCrop(BasicTransform):
    """
     Crops the center of the image with a fixed width and height.

     Parameters
     ----------
     height : int
         Height of the crop.
     width : int
         Width of the crop.
     """

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            x, y = im.shape[:2]
            x_center = x // 2
            y_center = y // 2
            if self.width > x or self.height > y:
                raise ValueError("We should have width<x and height<y")
            res.append((im[x_center - self.width // 2:x_center + self.width // 2,
                        y_center - self.height // 2:y_center + self.height // 2]))
        return res


class CropAndPad(BasicTransform):
    """
    Crops and pads the image. Crops the center of the image with a fixed width and height then adds a padding
    corresponding to the color value at the sides.

     Parameters
     ----------
     height : int
         Height of the crop.
     width : int
         Width of the crop.
     color_value : int
         Color of the padding.
     """

    def __init__(self, width, height, color_value):
        self.width = width
        self.height = height
        self.color_value = color_value

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            x, y = im.shape[:2]
            x_center = x // 2
            y_center = y // 2
            if self.width > x or self.height > y:
                raise ValueError("We should have width<x and height<y")
            tmp = im.copy()
            tmp[0:x_center - self.width // 2, :] = self.color_value
            tmp[x_center + self.width // 2: x, :] = self.color_value
            tmp[:, 0:y_center - self.height // 2] = self.color_value
            tmp[:, y_center + self.height // 2:y] = self.color_value
            res.append(tmp)
        return res


class RandomCrop(BasicTransform):
    """
     Randomly crops an area of the image with a fixed width and height.

     Parameters
     ----------
     height : int
         Height of the crop.
     width : int
         Width of the crop.

     """

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            x, y = im.shape[:2]
            if self.width > x or self.height > y:
                raise ValueError("We should have width<x and height<y")
            xmin = random.randint(0, x - self.width)
            ymin = random.randint(0, y - self.height)
            res.append(im[xmin:xmin + self.width, ymin:ymin + self.height])
        return res


class CropOrPad(BasicTransform):
    """
    Crops or pads the image to a fixed width and height. Crops the image if either the width or height is less than
    the initial width or height. Pads the images with the corresponding color value if either the width or height is
    more than the initial width or height.

     Parameters
     ----------
     height : int
         Height of the crop.
     width : int
         Width of the crop.
     color_value : int
         Color of the padding.
     """

    def __init__(self, width, height, color_value):
        self.width = width
        self.height = height
        self.color_value = color_value

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        x_center = self.width // 2
        y_center = self.height // 2
        for im in images:
            x, y = im.shape[:2]
            x_size = min(x, self.width) // 2
            y_size = min(y, self.height) // 2
            tmp = np.zeros([self.width, self.height, 3])
            tmp[:] = self.color_value
            tmp[x_center - x_size:x_center + x_size, y_center - y_size:y_center + y_size] = im[
                                                                                            x // 2 - x_size:x // 2 + x_size,
                                                                                            y // 2 - y_size:y // 2 + y_size]
            res.append(tmp)
        return res
