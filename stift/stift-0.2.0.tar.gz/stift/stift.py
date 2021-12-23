import math
import re
from typing import Any, Union

ANY_NUM_ARGS = "ANY_NUM_ARGS"
NUMERICAL = Union[int, float, complex]
REALS = Union[int, float]


# Identify strings

# Identify functions and arguments (recursive)
# This should first identify strings and exclude anything in them

# Process

# Function classes


def typechecker(x: str):
    # check if float, int, etc
    pass


class BaseFunction:
    def eval(s: str):
        """This function will evaluate a portion of another function."""
        pass

    def check_types():
        """Check arg types. If len arg_types = 1, all args must be of that type"""

    def init(self, *args):
        # preprocess array args
        self.argv = args
        self.argc = len(args)
        if (self.num_args != ANY_NUM_ARGS) and (self.argv not in self.num_args):
            pass
        #   raise FunctionError("Incorrect number of arguments")


class Sum(BaseFunction):
    arg_counts = ANY_NUM_ARGS
    arg_types = REALS

    def process(self):
        retval = 0
        for arg in self.args:
            retval += arg

        return retval


class Ceiling(BaseFunction):
    arg_counts = (1, 2)
    arg_types = REALS

    def process(self) -> REALS:
        if self.argc == 1:
            return math.ceil(self.argv[0])
        else:
            mult = self.argv[1]
            return math.ceil(self.argv[0] / mult) * mult


class Floor(BaseFunction):
    arg_counts = (1, 2)
    arg_types = REALS

    def process(self) -> REALS:
        if self.argc == 1:
            return math.floor(self.argv[0])
        else:
            mult = self.argv[1]
            return math.floor(self.argv[0] / mult) * mult


class Round(BaseFunction):
    arg_counts = (1, 2)
    arg_types = REALS

    def process(self) -> REALS:
        if self.argc == 1:
            return round(self.argv[0])
        else:
            mult = self.argv[1]
            return round(self.argv[0], self.argv[1])


class Trunc(BaseFunction):
    arg_counts = (1, 2)

    def process(self):
        pass


class Today(BaseFunction):
    pass


class Hour(BaseFunction):
    pass


class Minute(BaseFunction):
    pass


class Month(BaseFunction):
    pass


class If(BaseFunction):
    pass


class Coalesce(BaseFunction):
    """Not technically a spreadsheet function, but possibly very useful"""

    pass


class Concatenate(BaseFunction):
    pass


class Trim(BaseFunction):
    pass


class Len(BaseFunction):
    pass


class Stift:
    """Parent class."""

    function_cls_map = {"sum": Sum}

    def __init__(self, s: str, allowed_variables: list = None):
        self.s = s

        self.allowed_variables = allowed_variables if allowed_variables is None else []

    def add_function():
        pass

    def parse():
        """Find lowest level functions, execute those first.

        Then work up."""
        pass
