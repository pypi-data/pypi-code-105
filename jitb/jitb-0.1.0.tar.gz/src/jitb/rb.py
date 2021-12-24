__all__ = [
    "chance",
    "either"
]


def chance(chance: float, value):
    from random import random
    return value if random() < chance / 100 else None


def either(a, b = None):
    from random import choice
    return choice((a, b))

