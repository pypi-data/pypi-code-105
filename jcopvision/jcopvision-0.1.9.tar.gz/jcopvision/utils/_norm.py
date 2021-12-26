import numpy as np


def normalize_pixel(image):
    if image.dtype == np.uint8:
        return image / 255
    else:
        return image
