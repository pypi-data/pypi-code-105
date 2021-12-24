# -*- coding: utf-8 -*-
import re
import unittest
from datetime import timedelta, datetime

import pytz

from raccoon_simple_stopwatch.stopwatch import StopWatch


class InitialStateTests(unittest.TestCase):
    def test_none_start_time_by_default(self):
        sw = StopWatch()
        self.assertIsNone(sw.start_datetime)

    def test_none_stop_time_by_default(self):
        sw = StopWatch()
        self.assertIsNone(sw.stop_datetime)

    def test_none_elapsed_by_default(self):
        sw = StopWatch()
        self.assertIsNone(sw.elapsed())

    def test_not_none_start_time_after_auto_start(self):
        sw = StopWatch(auto_start=True)
        self.assertIsNotNone(sw.start_datetime)

    def test_none_stop_time_after_auto_start(self):
        sw = StopWatch(auto_start=True)
        self.assertIsNone(sw.stop_datetime)

    def test_not_none_elapsed_after_auto_start(self):
        sw = StopWatch(auto_start=True)
        self.assertIsNotNone(sw.elapsed())

    def test_not_none_start_time_after_start(self):
        sw = StopWatch()
        sw.start()
        self.assertIsNotNone(sw.start_datetime)

    def test_none_stop_time_after_start(self):
        sw = StopWatch()
        sw.start()
        self.assertIsNone(sw.stop_datetime)

    def test_not_none_elapsed_after_start(self):
        sw = StopWatch()
        sw.start()
        self.assertIsNotNone(sw.elapsed())


class ElapsedTimeTests(unittest.TestCase):
    def test_default_type(self):
        sw = StopWatch(auto_start=True)
        elapsed_time = sw.elapsed()
        self.assertTrue(isinstance(elapsed_time, str))

    def test_raw_type(self):
        sw = StopWatch(auto_start=True)
        elapsed_time = sw.elapsed(raw=True)
        self.assertTrue(isinstance(elapsed_time, timedelta))

    def test_time_is_running(self):
        sw = StopWatch(auto_start=True)
        elapsed_time_1 = sw.elapsed(raw=True)
        elapsed_time_2 = sw.elapsed(raw=True)
        self.assertGreater(elapsed_time_2.microseconds, elapsed_time_1.microseconds)

    def test_elapsed_matches_pattern(self):
        sw = StopWatch(auto_start=True)
        elapsed_time = sw.elapsed()
        matched = re.match(r"\d\.\d{1,2}:\d{2}:\d{2}\.\d+", elapsed_time)
        matched_short = re.match(r"\d{1,2}:\d{2}:\d{2}\.\d+", elapsed_time)
        self.assertTrue(matched is not None or matched_short is not None)


class StartDateTimeTests(unittest.TestCase):
    def test_type(self):
        sw = StopWatch(auto_start=True)
        self.assertTrue(isinstance(sw.start_datetime, datetime))

    def test_tz_unaware_local(self):
        sw = StopWatch(auto_start=True)
        self.assertIsNone(sw.start_datetime.tzinfo)

    def test_tz_unaware_utc(self):
        sw = StopWatch(auto_start=True, use_utc=True)
        self.assertIsNone(sw.start_datetime.tzinfo)

    def test_tz_aware_local(self):
        sw = StopWatch(auto_start=True, make_tz_aware=True)

        # Since I don`t where this test is going to run, not going to validate the content of tzinfo.
        self.assertIsNotNone(sw.start_datetime.tzinfo)

    def test_tz_aware_utc(self):
        sw = StopWatch(auto_start=True, use_utc=True, make_tz_aware=True)
        self.assertEqual(pytz.UTC, sw.start_datetime.tzinfo)


class StopDateTimeTests(unittest.TestCase):
    def test_type(self):
        sw = StopWatch(auto_start=True)
        sw.end()
        self.assertTrue(isinstance(sw.stop_datetime, datetime))

    def test_tz_unaware_local(self):
        sw = StopWatch(auto_start=True)
        sw.end()
        self.assertIsNone(sw.stop_datetime.tzinfo)

    def test_tz_unaware_utc(self):
        sw = StopWatch(auto_start=True, use_utc=True)
        sw.end()
        self.assertIsNone(sw.stop_datetime.tzinfo)

    def test_tz_aware_local(self):
        sw = StopWatch(auto_start=True, make_tz_aware=True)
        sw.end()
        # Since I don`t where this test is going to run, not going to validate the content of tzinfo.
        self.assertIsNotNone(sw.stop_datetime.tzinfo)

    def test_tz_aware_utc(self):
        sw = StopWatch(auto_start=True, use_utc=True, make_tz_aware=True)
        sw.end()
        self.assertEqual(pytz.UTC, sw.stop_datetime.tzinfo)


if __name__ == '__main__':
    unittest.main()
