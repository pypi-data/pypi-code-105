class RawCollision():

    def __init__(self, **kwargs):
        self.data = kwargs

    @staticmethod
    def parse(data):
        if isinstance(data, RawCollision):
            return data

        return RawCollision(
            **data
        )
