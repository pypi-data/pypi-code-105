from typing import Any, Iterable, Union, get_args

from stift.exceptions import FunctionError

ANY_NUM_ARGS = "ANY_NUM_ARGS"
ANY = Any
NUMERICAL = Union[int, float, complex]
REALS = Union[int, float]


class BaseFunction:
    """Basic function class meant to be overloaded.

    arg_counts, arg_types, and process() need to be defined."""

    arg_counts = None
    arg_types = None

    @classmethod
    def getfuncname(cls):
        """Name we will call this function by.

        Defaults to the class name in lowercase. This function can be
        overridden in derived classes."""
        return cls.__name__.lower()

    def __init__(self):
        self.funcname = self.getfuncname()

    def execute(self, *args):
        self.argv = args
        self.argc = len(args)
        self.check_arg_count()
        self.check_arg_types()
        return self.process(argc=self.argc, argv=self.argv)

    def check_arg_count(self):
        """Verify the proper number of arguments"""
        if self.argc < 1:
            raise FunctionError(f"{self.funcname}() expected arguments: none given")

        if self.arg_counts == ANY_NUM_ARGS:
            pass
        elif isinstance(self.arg_counts, Iterable):
            if self.argc not in self.arg_counts:
                arglist = ", ".join(self.arg_counts[:-1])
                arglist = (
                    f"{arglist} or {self.arg_counts[-1]}"
                    if len(self.arg_counts) > 1
                    else arglist
                )
                raise FunctionError(
                    f"{self.funcname}() expected {arglist} argument(s): {self.argc} given"
                )
        else:
            if self.argc != self.arg_counts:
                raise FunctionError(
                    f"{self.funcname}() expected {self.arg_counts} argument(s): {self.argc} given"
                )

        # Verify the proper type of arguments

    def check_arg_types(self):
        """Check arg types. If len arg_types = 1, all args must be of that type"""

        if isinstance(self.arg_types, Iterable) and len(self.arg_types) == 1:
            self.arg_types = self.arg_types[0]

        if isinstance(self.arg_types, Iterable):
            for i, arg in enumerate(self.argv):
                if not isinstance(arg, get_args(self.arg_types[i])):
                    raise FunctionError(
                        f"{self.funcname}() expected type {self.arg_types[i]} at position {i}: got {type(arg)}"
                    )

        else:
            for i, arg in enumerate(self.argv):
                if not isinstance(arg, get_args(self.arg_types)):
                    raise FunctionError(
                        f"{self.funcname}() expected type {self.arg_types} at position {i}: got {type(arg)}"
                    )

    def process(self, argc: int, argv: list):
        raise NotImplementedError
