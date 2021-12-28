from typing import List


class Result(object):
    def __init__(self):
        self.type = self.__type__()

    def __type__(self) -> str:
        raise NotImplementedError(f'Method __type__() not implemented in {self.__name__}')

    def is_success(self) -> bool:
        raise NotImplementedError(f'Method is_success() not implemented in {self.__name__}')


class Success(Result):
    def __init__(self, value):
        super().__init__()
        if value is None:
            raise ValueError(f'value cannot be None in {self.__name__}')
        self.value = value

    def is_success(self) -> bool:
        return True


class Failure(Result):
    def __init__(self, error):
        super().__init__()
        self.error = error

    def is_success(self) -> bool:
        return False

    def __type__(self) -> str:
        return 'failure'


class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Labeled(object):
    def __init__(self, label: str):
        self.label = label


class BoundingBox(Labeled):
    def __init__(self, top_left_coordinate: Coordinate, bottom_right_coordinate: Coordinate,
                 confidence: float, label: str):
        super().__init__(label)
        self.top_left_coordinate = top_left_coordinate
        self.bottom_right_coordinate = bottom_right_coordinate
        self.width = bottom_right_coordinate.x - top_left_coordinate.x
        self.height = bottom_right_coordinate.y - top_left_coordinate.y
        self.confidence = confidence


class ObjectDetectionResult(Success):
    def __init__(self, bounding_boxes: List[BoundingBox]):
        super().__init__(bounding_boxes)

    def __type__(self) -> str:
        return 'object_detection'


class SegmentationMask(Labeled):
    def __init__(self, coordinates: List[Coordinate], label: str):
        super().__init__(label)
        self.coordinates = coordinates


class SegmentationResult(Success):
    def __init__(self, segmentation: SegmentationMask):
        super().__init__(segmentation)

    def __type__(self) -> str:
        return 'segmentation'


class Classification(Labeled):
    def __init__(self, label: str, confidence: float):
        super().__init__(label)
        self.confidence = confidence


class ClassificationResult(Success):
    def __init__(self, classifications: List[Classification]):
        super().__init__(classifications)

    def __type__(self) -> str:
        return 'classification'


class ImageResult(Success):
    def __init__(self, image: bytes):
        super().__init__(image)

    def __type__(self) -> str:
        return 'image'


class TextResult(Success):
    def __init__(self, text: str):
        super().__init__(text)

    def __type__(self) -> str:
        return 'text'


class NamedResult(Result):
    def __init__(self, name: str, result: Result):
        self.name = name
        self.result = result
        super().__init__()

    def __type__(self) -> str:
        return self.result.type

    def is_success(self) -> bool:
        return self.result.is_success()


class CompositeResult(Result):
    def __init__(self, results: List[NamedResult]):
        self.results = results
        super().__init__()

    def __type__(self) -> str:
        return 'composite'

    def is_success(self) -> bool:
        return all(map(lambda x: x.is_success(), self.results))


class GenericResult(Success):
    def __init__(self, value):
        super().__init__(value)

    def __type__(self) -> str:
        return 'generic'


class GenericArrayResult(GenericResult):
    def __init__(self, value: List):
        super().__init__(value)

    def __type__(self) -> str:
        return 'generic_array'
