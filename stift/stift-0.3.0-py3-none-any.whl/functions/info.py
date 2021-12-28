from typing import get_args

from stift.functions.base import ANY, ANY_NUM_ARGS, REALS, BaseFunction


class IsNumber(BaseFunction):
    """Check if the type is not a string."""

    arg_counts = 1
    arg_types = ANY

    def process(self, argc: int, argv: list) -> bool:
        return not isinstance(argv[0], str)


class IsNumber(BaseFunction):
    """Check if the type is a number."""

    arg_counts = 1
    arg_types = ANY

    def process(self, argc: int, argv: list) -> bool:
        return isinstance(argv[0], get_args(REALS))


class IsText(BaseFunction):
    """Check if the type is text."""

    arg_counts = 1
    arg_types = ANY

    def process(self, argc: int, argv: list) -> bool:
        return isinstance(argv[0], str)


class Type(BaseFunction):
    """Return the type of the argument."""

    arg_counts = 1
    arg_types = ANY

    def process(self, argc: int, argv: list) -> bool:
        return type(argv[0])
