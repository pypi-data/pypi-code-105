import sys; sys.path.append('..');
import unittest

from iinput import utils


class UtilsTest(unittest.TestCase):


    def test_isfloat(self):
        test_data = {
            " 1.0 ": True,
            "1.0": True,
            "-1.0": True,
            ".0": True,
            "1": False,
            "-1": False,
            "a": False,
            " ": False,
            "": False,
        }
        for string, expected_truth in test_data.items():
            self.assertEqual(utils.isfloat(string), expected_truth)


    def test_isint(self):
        test_data = {
            '1': True,
            '+1': True,
            '-1': True,
            '--1': True,
            '++1': True,
            '+-1': True,
            '1.0': False,
            '': False,
            ' ': False,
        }
        for string, expected_truth in test_data.items():
            self.assertEqual(utils.isint(string), expected_truth)


    def test_ischar(self):
        test_data = {
            " a ": False,
            "a": True,
            "ab": False,
            " ": True,
            "": False,
            1: False,
        }
        for string, expected_truth in test_data.items():
            self.assertEqual(utils.ischar(string), expected_truth)


    def test_interpret_type(self):
        test_data = {
            " True ": bool,
            "True": bool,
            "true": bool,
            "False": bool,
            "false": bool,
            "123": int,
            "0": int,
            "1": int,
            "123.4": float,
            "abc": str,
            "123abc": str,
            "None": None,
            '  ': None,
            '': None,
        }
        for string, expected_type in test_data.items():
            self.assertEqual(utils.interpret_type(string), expected_type)


    def test_auto_cast(self):
        test_data = [
            (['abc', '123', '123.4', 'False', 'True'], [str], ['abc', '123', '123.4', 'False', 'True']),
            (['abc', '123', '123.4', 'False', 'True'], [str, int], ['abc', 123, '123.4', 'False', 'True']),
            (['abc', '123', '123.4', 'False', 'True'], [str, int, float], ['abc', 123, 123.4, 'False', 'True']),
            (['abc', '123', '123.4', 'False', 'True'], [str, int, float, bool], ['abc', 123, 123.4, False, True]),
            ([' abc ', ' 123 ', ' 123.4 ', ' False ', ' True '], [str, int, float, bool], ['abc', 123, 123.4, False, True]),
            (['abc', '123', '123.4', 'False', 'True'], [int], [None, 123, None, None, None]),
            (['0', '1'], [int], [0, 1]),
            (['-1', '2'], [int], [-1, 2]),
            (['0', '1'], [bool], [False, True]),
            (['0', '1'], [int, bool], [0, 1]),
            (['0', '1', '2'], [bool], [False, True, None]),
            (['0', '1', '2'], [int, bool], [0, 1, 2]),
            ([], [str, int, float, bool], []),
            ([], [], []),
        ]
        for items, allowed_types, expected_values in test_data:
            self.assertEqual(utils.auto_cast(items, allowed_types=allowed_types), expected_values)


    def test_split_ws(self):
        test_data = {
            '': [],
            ' ': [],
            ' ,,,': [],
            ' 1': ['1'],
            ' 1 ': ['1'],
            ' 1,2,  3, 45, ': ['1', '2', '3', '45'],
            ' 1,2,  3, 45, ,': ['1', '2', '3', '45'],
            ', 1,2,  3, 45, ,': ['1', '2', '3', '45'],
        }
        for string, split in test_data.items():
            self.assertEqual(utils.split_ws(string, delimiter=','), split)


if __name__ == '__main__':
    unittest.main()
