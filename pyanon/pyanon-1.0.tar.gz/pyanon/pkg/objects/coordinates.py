class Coordinates:
    def __init__(self, latitude: float, longitude: float, zoom: int) -> None:
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.zoom: int = zoom