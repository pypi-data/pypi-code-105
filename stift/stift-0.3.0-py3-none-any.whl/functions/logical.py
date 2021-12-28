from typing import Any

from stift.functions.base import ANY, ANY_NUM_ARGS, REALS, BaseFunction


class And(BaseFunction):
    """Check if all arguments are true."""

    arg_counts = ANY_NUM_ARGS
    arg_types = ANY

    def process(self, argc: int, argv: list) -> bool:
        for arg in argv:
            if not bool(arg):
                return False

        return True


class If(BaseFunction):
    """Standard if(expression, if_true, if_false) function"""

    arg_counts = 3
    arg_types = ANY

    def process(self, argc: int, argv: list) -> Any:
        if bool(argv[0]):
            return argv[1]
        return argv[2]


class Not(BaseFunction):
    """Return the opposite."""

    arg_counts = 1
    arg_types = ANY

    def process(self, argc: int, argv: list) -> bool:
        return not bool(argv[0])


class Or(BaseFunction):
    """Check if any arguments are true."""

    arg_counts = ANY_NUM_ARGS
    arg_types = ANY

    def process(self, argc: int, argv: list) -> bool:
        for arg in argv:
            if bool(arg):
                return True

        return False
