"""test_functions.py

Unit testing on stift's functions"""
import stift.functions as funcs


class TestMathFunctions:
    def test_abs(self):
        assert funcs.Abs().execute(-4.5) == 4.5
        assert funcs.Abs().execute(4.5) == 4.5
