import pytest
from deepdiff import DeepDiff
from stift.parser import Parser, ParserError, ParseTypes


class TestParser:
    def test_simple(self):
        s = r"""b("a",s[0])"""
        parsed = Parser(fmtstr=False).parse(s)

        expected = [
            [
                {
                    "type": ParseTypes.function,
                    "value": "b",
                    "argc": 2,
                    "argv": [(1, 0), (1, 1)],
                }
            ],
            [
                {"type": str, "value": "a"},
                {"type": ParseTypes.array, "value": "s", "index": (2, 0)},
            ],
            [{"type": int, "value": 0}],
        ]

        assert DeepDiff(parsed, expected) == {}

    def test_complex(self):
        s = r"""func1(val1, func2(1, 2, "\"yes\" (or) \"no\"", arr1[func3(arr2[2])]), "{[(str2")"""
        parsed = Parser(fmtstr=False).parse(s)

        expected = [
            [
                {
                    "type": ParseTypes.function,
                    "value": "func1",
                    "argc": 3,
                    "argv": [(1, 0), (1, 1), (1, 2)],
                }
            ],
            [
                {"type": ParseTypes.variable, "value": "val1"},
                {
                    "type": ParseTypes.function,
                    "value": "func2",
                    "argc": 4,
                    "argv": [(2, 0), (2, 1), (2, 2), (2, 3)],
                },
                {"type": str, "value": "{[(str2"},
            ],
            [
                {"type": int, "value": 1},
                {"type": int, "value": 2},
                {"type": str, "value": '"yes" (or) "no"'},
                {"type": ParseTypes.array, "value": "arr1", "index": (3, 0)},
            ],
            [
                {
                    "type": ParseTypes.function,
                    "value": "func3",
                    "argc": 1,
                    "argv": [(4, 0)],
                },
            ],
            [
                {"type": ParseTypes.array, "value": "arr2", "index": (5, 0)},
            ],
            [
                {"type": int, "value": 2},
            ],
        ]

        assert DeepDiff(parsed, expected) == {}

    def test_meta(self):
        """Test meta tags starting with @@. Make sure they don't get flagged as bad identifiers."""
        s = r"""@@b("a")"""
        parsed = Parser(fmtstr=False).parse(s)

        expected = [
            [
                {
                    "type": ParseTypes.function,
                    "value": "@@b",
                    "argc": 1,
                    "argv": [(1, 0)],
                }
            ],
            [
                {"type": str, "value": "a"},
            ],
        ]

        assert DeepDiff(parsed, expected) == {}


class TestParserFormat:
    """Test parser with the format string option"""

    def test_simple(self):
        s = r"""This is a test format string {b("a",s[0])} like this {"abc"}"""
        parsed = Parser(fmtstr=True).parse(s)

        expected = [
            [
                {"type": str, "value": "This is a test format string "},
                {
                    "type": ParseTypes.function,
                    "value": "b",
                    "argc": 2,
                    "argv": [(1, 0), (1, 1)],
                },
                {"type": str, "value": " like this "},
                {"type": str, "value": "abc"},
            ],
            [
                {"type": str, "value": "a"},
                {"type": ParseTypes.array, "value": "s", "index": (2, 0)},
            ],
            [{"type": int, "value": 0}],
        ]

        assert DeepDiff(parsed, expected) == {}


class TestParserErrors:
    def test_missing_closing(self):
        """Test with missing closing bracket"""
        s = r"""func(12"""
        with pytest.raises(ParserError):
            Parser(fmtstr=False).parse(s)

    def test_invalid_identifier(self):
        """Verify it catches a bad identifier"""
        s = r"""fu nc(12)"""
        with pytest.raises(ParserError):
            Parser(fmtstr=False).parse(s)
