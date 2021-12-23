from .basic_transform import BasicTransform
from typing import List
import numpy as np
import random
import math


class Identity(BasicTransform):
    """
    Does not change the input images
    """

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        return images


class Transpose(BasicTransform):
    """
     Transposes the image.
     """

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            res.append(np.transpose(im, (1, 0, 2)))
        return res


class RandomRotation90(BasicTransform):
    """
     Rotates the image by 90 degrees, from 0 to 3 times

     Parameters
     ----------
     factor : int
         Number of times the image will be rotated. You can choose a value between 0 or 3 or leave it random if you don't specify.
     """

    def __init__(self, factor=random.randint(0, 3)):
        self.factor = factor

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            switcher = {
                0: im,
                1: np.transpose(im, (1, 0, 2))[:, ::-1, :],
                2: np.transpose(im, (1, 0, 2))[::-1, :, :],
                3: im[::-1, :, :]
            }
            res.append(switcher.get(self.factor))
        return res


class Rotation(BasicTransform):
    """
     Rotates the image by angle using a pivot point

     Parameters
     ----------
     angle: float
            angle in degrees
     """

    def __init__(self, angle):
        self.angle = math.radians(angle)
        self.cos = np.cos(self.angle)
        self.sin = np.sin(self.angle)

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            height, width = im.shape[:2]
            piv_x = width // 2
            piv_y = height // 2
            new_img = np.zeros(im.shape)
            rotation = np.transpose(np.array([[self.cos, -self.sin], [self.sin, self.cos]]))
            for i in range(height):
                for j in range(width):
                    xy_mat = np.array([[j - piv_x], [i - piv_y]])
                    rotation_mat = np.dot(rotation, xy_mat)
                    new_x = piv_x + int(rotation_mat[0])
                    new_y = piv_y + int(rotation_mat[1])
                    if (0 <= new_x <= width - 1) and (0 <= new_y <= height - 1):
                        new_img[new_y, new_x, :] = im[i, j, :]
            res.append(new_img)
        return res
