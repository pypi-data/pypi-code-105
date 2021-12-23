import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point2):
        dx = self.x - point2.x
        dy = self.y - point2.y
        return math.sqrt(dx * dx + dy * dy)