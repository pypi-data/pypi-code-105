"""test_stift.py

Integration tests for stift"""

from stift import Stift


class TestStift:
    def test_stift(self):
        st = Stift()
        s = r"""{sum(1,2,3)}"""
        res = st.parse(s)
        assert res == "6"

        res = st.parse("This is how it works! {ceiling(sum(4,0.3,0.8))}")
        assert res == "This is how it works! 6"
