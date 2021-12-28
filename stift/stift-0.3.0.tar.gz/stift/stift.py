import inspect
import re

import stift.functions as funcs

# import stift.functions
from stift.parser import Parser, ParseTypes, tupindex

# s = Sum()
# print(s._funcname())


def get_functions() -> dict:
    """Get all classes in the funcs module."""
    func_classes = inspect.getmembers(funcs, inspect.isclass)

    return {
        m[1].getfuncname(): m[1]
        for m in func_classes
        if (funcs.__name__ in m[1].__module__ and m[1].getfuncname() != "basefunction")
    }


class Stift:
    """Parent class."""

    function_cls_map = get_functions()

    def __init__(self, s: str = None, allowed_variables: list = None):
        self.s = s

        self.allowed_variables = allowed_variables if allowed_variables is None else []

    def add_function(self, cls):
        """Add a new function to the list"""
        self.function_class_map[cls.getfuncname()] = cls

    def parse(self, s: str = None, fmtstr: bool = True):
        """Find lowest level functions, execute those first.

        Then work up."""

        if s is not None:
            self.s = s
        else:
            s = self.s

        parsed = Parser(fmtstr=fmtstr).parse(s)

        for i, level in enumerate(reversed(parsed)):
            for j, token in enumerate(level):
                if token["type"] == ParseTypes.variable:
                    token["value"] = self.allowed_variables[token["value"]]
                elif token["type"] == ParseTypes.array:
                    arr = token["value"]
                    index = tupindex(parsed, token["index"])["value"]
                    token["value"] = self.allowed_variables[arr][index]
                elif token["type"] == ParseTypes.function:
                    argv = [tupindex(parsed, t)["value"] for t in token["argv"]]
                    Func = self.function_cls_map[token["value"]]
                    token["value"] = Func().execute(*argv)

        return "".join([str(t["value"]) for t in parsed[0]])
