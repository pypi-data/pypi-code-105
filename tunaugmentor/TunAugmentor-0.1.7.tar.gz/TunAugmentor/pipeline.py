import numpy
from .transformations.basic_transform import BasicTransform
from typing import List

class Pipeline ():
    transformations: List[BasicTransform] = []

    def __init__(self, transformations: List[BasicTransform]):
        for transformation in transformations:
            if not(isinstance(transformation,BasicTransform)):
                raise TypeError
        self.transformations=transformations
    def arrange(self,images: List[numpy.ndarray]):
        for transformation in self.transformations:
            images=images+transformation.transform(images)
        return images
    def apply(self,images: List[numpy.ndarray]):
        res=images.copy()
        for transformation in self.transformations:
            res=res+transformation.transform(images)
        return res