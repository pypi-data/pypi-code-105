import numpy
from .transformations.basic_transform import BasicTransform
from typing import List
from .logger import logger


class Pipeline:
    """
    Image Augmentation Pipeline. Applies a list of transformations on a list of images. Either applies them to a list
    of original images or composes the transformations to get 2 to the power of n images.

     Methods
     -------
     arrange(images: List[numpy.ndarray):
         Composes the transformations to a list of images.
     apply(images: List[numpy.ndarray):
         Applies the transformations to a list of images
    """

    transformations: List[BasicTransform] = []
    logging_enabled: bool

    def __init__(self, transformations: List[BasicTransform], **kwargs):
        for transformation in transformations:
            if not (isinstance(transformation, BasicTransform)):
                raise TypeError
        self.transformations = transformations
        logging = kwargs.get("logging_enabled")
        if not logging:
            self.logging_enabled = logging
        else:
            self.logging_enabled = True

    def arrange(self, images: List[numpy.ndarray]):
        for transformation in self.transformations:
            images = images + transformation.transform(images)
            if self.logging_enabled:
                logger.info("Applying " + transformation.__class__.__name__ + " on " + str(len(images)) + " images")
        logger.info("Completed")
        return images

    def apply(self, images: List[numpy.ndarray]):
        res = images.copy()
        for transformation in self.transformations:
            logger.info("Applying " + transformation.__class__.__name__ + " on " + str(len(images)) + " images")
            res = res + transformation.transform(images)
        logger.info("Completed")
        return res
