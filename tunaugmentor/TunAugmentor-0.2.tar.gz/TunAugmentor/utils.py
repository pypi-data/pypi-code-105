import cv2
import glob
from .logger import logger


def read_images(path):
    """
    Reads a list of jpg images from a path

            Parameters:
                    path(str) :path to images folder

            Returns:
                    images (List[numpy.ndarray]): list of numpy arrays containing the images
    """

    images = []
    files = glob.glob(path + "/*.jpg")
    for myFile in files:
        image = cv2.imread(myFile)
        images.append(image)
    return images


def read_image(path):
    """
    Reads a single image from a path and appends it to a list

            Parameters:
                    path(str) :path to images folder

            Returns:
                    images (List[numpy.ndarray]): list containing the single image.
    """

    image = [cv2.imread(path)]
    return image


def export(images, path, base="img", **kwargs):
    """
    Export images from a list of numpy arrays to a path.

            Parameters:
                    path(str): path to export to.
                    base(str): base name for the image
                    logging_enabled(bool), optional: enables logging

            Returns:
                    images (List[numpy.ndarray]): list containing the single image.
    """

    i = 0
    res = True
    logging = kwargs.get("logging_enabled")
    if not logging:
        logging_enabled = logging
    else:
        logging_enabled = True

    for im in images:
        i += 1
        img_name = '/' + base + str(i) + '.jpg'
        if logging_enabled:
            logger.info("Exporting" + base + str(i) + ".jpg")
        res = cv2.imwrite(path + img_name, im) and res
    return res
