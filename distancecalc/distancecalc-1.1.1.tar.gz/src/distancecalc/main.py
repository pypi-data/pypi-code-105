import math


def distance(p1x, p1y, p2x, p2y):
    dx = p1x - p2x
    dy = p1y - p2y
    return math.sqrt(dx * dx + dy * dy)
