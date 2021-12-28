import cv2
import base64
import numpy as np
from typing import List


class Input(object):
    def __init__(self, data):
        self.type = self.__type__()
        self.data = data

    def __type__(self) -> str:
        raise NotImplementedError(f'Method __type__() not implemented in {self.__name__}')


class ImageInput(Input):
    def __init__(self, base64_image: str):
        super().__init__(base64_image)

    def __type__(self):
        return 'image'

    @classmethod
    def from_cv2_image(cls, cv2_image):
        _, buffer = cv2.imencode('.jpg', cv2_image)
        return ImageInput(base64.b64encode(buffer).decode('utf-8'))

    @classmethod
    def from_pillow_image(cls, pillow_image):
        open_cv_image = np.array(pillow_image)
        cv2_image = open_cv_image[:, :, ::-1].copy()
        return cls.from_cv2_image(cv2_image)

    @classmethod
    def from_file(cls, file_path):
        return cls.from_cv2_image(cv2.imread(file_path))


class TextInput(Input):
    def __init__(self, text: str):
        super().__init__(text)

    def __type__(self):
        return 'text'


class GenericInput(Input):
    def __init__(self, data):
        super().__init__(data)

    def __type__(self) -> str:
        return 'generic'


class GenericArrayInput(GenericInput):
    def __init__(self, data: List):
        super().__init__(data)

    def __type__(self) -> str:
        return 'generic_array'


class NamedInput(Input):
    def __init__(self, name: str, input: Input):
        self.name = name
        self.input = input
        super().__init__(input.data)

    def __type__(self) -> str:
        return self.input.type


class CompositeInput(Input):
    def __init__(self, inputs: List[NamedInput]):
        result = {}
        for i in inputs:
            result[i.name] = i.input.data
        super().__init__(result)

    def __type__(self) -> str:
        return 'composite'

# TODO SoundInput(sound en formato estandar, metadata)
