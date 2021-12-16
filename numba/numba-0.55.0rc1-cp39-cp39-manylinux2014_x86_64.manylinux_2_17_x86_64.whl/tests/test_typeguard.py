"""
Tests to ensure that typeguard is working as expected.
This mostly contains negative tests as proof that typeguard can catch errors.
"""
import unittest
from numba.tests.support import TestCase, skip_unless_typeguard


def guard_args(val: int):
    return


def guard_ret(val) -> int:
    return val


@skip_unless_typeguard
class TestTypeGuard(TestCase):
    def test_check_args(self):
        with self.assertRaises(TypeError):
            guard_args(float(1.2))

    def test_check_ret(self):
        with self.assertRaises(TypeError):
            guard_ret(float(1.2))

    def test_check_does_not_work_with_inner_func(self):
        def guard(val: int) -> int:
            return

        guard(float(1.2))


if __name__ == '__main__':
    unittest.main()
