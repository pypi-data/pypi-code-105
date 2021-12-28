import math

from stift.functions.base import ANY_NUM_ARGS, REALS, BaseFunction


class Abs(BaseFunction):
    """Math absolute value function."""

    arg_counts = 1
    arg_types = REALS

    def process(self, argc: int, argv: list) -> REALS:
        return abs(argv[0])


class Ceiling(BaseFunction):
    """Math ceiling function."""

    arg_counts = (1, 2)
    arg_types = REALS

    def process(self, argc: int, argv: list) -> REALS:
        if argc == 1:
            return math.ceil(argv[0])
        else:
            mult = argv[1]
            return math.ceil(argv[0] / mult) * mult


class Floor(BaseFunction):
    """Math floor function."""

    arg_counts = (1, 2)
    arg_types = REALS

    def process(self, argc: int, argv: list) -> REALS:
        if argc == 1:
            return math.floor(argv[0])
        else:
            mult = argv[1]
            return math.floor(argv[0] / mult) * mult


class Round(BaseFunction):
    """Round to a given number of digits."""

    arg_counts = (1, 2)
    arg_types = REALS

    def process(self, argc: int, argv: list) -> REALS:
        if argc == 1:
            return round(argv[0])
        else:
            return round(argv[0], argv[1])


class Sum(BaseFunction):
    """Sum all arguments."""

    arg_counts = ANY_NUM_ARGS
    arg_types = REALS

    def process(self, argc: int, argv: list):
        retval = 0
        for arg in argv:
            retval += arg

        return retval


class Trunc(BaseFunction):
    arg_counts = (1, 2)

    def process(self, argc: int, argv: list):
        raise NotImplementedError
