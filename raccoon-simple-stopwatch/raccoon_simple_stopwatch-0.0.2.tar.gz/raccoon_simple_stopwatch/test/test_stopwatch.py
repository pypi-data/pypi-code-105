# -*- coding: utf-8 -*-
import re
import unittest
from datetime import timedelta, datetime
import pytz

from raccoon_simple_stopwatch.stopwatch import StopWatch


class InitialStateTests(unittest.TestCase):
    def test_none_start_time_by_default(self):
        stop_watch = StopWatch()
        self.assertIsNone(stop_watch.start_datetime)

    def test_none_stop_time_by_default(self):
        stop_watch = StopWatch()
        self.assertIsNone(stop_watch.stop_datetime)

    def test_none_elapsed_by_default(self):
        stop_watch = StopWatch()
        self.assertIsNone(stop_watch.elapsed())

    def test_not_none_start_time_after_auto_start(self):
        stop_watch = StopWatch(auto_start=True)
        self.assertIsNotNone(stop_watch.start_datetime)

    def test_none_stop_time_after_auto_start(self):
        stop_watch = StopWatch(auto_start=True)
        self.assertIsNone(stop_watch.stop_datetime)

    def test_not_none_elapsed_after_auto_start(self):
        stop_watch = StopWatch(auto_start=True)
        self.assertIsNotNone(stop_watch.elapsed())

    def test_not_none_start_time_after_start(self):
        stop_watch = StopWatch()
        stop_watch.start()
        self.assertIsNotNone(stop_watch.start_datetime)

    def test_none_stop_time_after_start(self):
        stop_watch = StopWatch()
        stop_watch.start()
        self.assertIsNone(stop_watch.stop_datetime)

    def test_not_none_elapsed_after_start(self):
        stop_watch = StopWatch()
        stop_watch.start()
        self.assertIsNotNone(stop_watch.elapsed())


class ElapsedTimeTests(unittest.TestCase):
    def test_default_type(self):
        stop_watch = StopWatch(auto_start=True)
        elapsed_time = stop_watch.elapsed()
        self.assertTrue(isinstance(elapsed_time, str))

    def test_raw_type(self):
        stop_watch = StopWatch(auto_start=True)
        elapsed_time = stop_watch.elapsed(raw=True)
        self.assertTrue(isinstance(elapsed_time, timedelta))

    def test_time_is_running(self):
        stop_watch = StopWatch(auto_start=True)
        elapsed_time_1 = stop_watch.elapsed(raw=True)
        elapsed_time_2 = stop_watch.elapsed(raw=True)
        self.assertGreater(elapsed_time_2.microseconds, elapsed_time_1.microseconds)

    def test_elapsed_matches_pattern(self):
        stop_watch = StopWatch(auto_start=True)
        elapsed_time = stop_watch.elapsed()
        matched = re.match(r"\d\.\d{1,2}:\d{2}:\d{2}\.\d+", elapsed_time)
        matched_short = re.match(r"\d{1,2}:\d{2}:\d{2}\.\d+", elapsed_time)
        self.assertTrue(matched is not None or matched_short is not None)


class StartDateTimeTests(unittest.TestCase):
    def test_type(self):
        stop_watch = StopWatch(auto_start=True)
        self.assertTrue(isinstance(stop_watch.start_datetime, datetime))

    def test_tz_unaware_local(self):
        stop_watch = StopWatch(auto_start=True)
        self.assertIsNone(stop_watch.start_datetime.tzinfo)

    def test_tz_unaware_utc(self):
        stop_watch = StopWatch(auto_start=True, use_utc=True)
        self.assertIsNone(stop_watch.start_datetime.tzinfo)

    def test_tz_aware_local(self):
        stop_watch = StopWatch(auto_start=True, make_tz_aware=True)

        # Since I don`t where this test is going to run, not going to validate the content of tzinfo.
        self.assertIsNotNone(stop_watch.start_datetime.tzinfo)

    def test_tz_aware_utc(self):
        stop_watch = StopWatch(auto_start=True, use_utc=True, make_tz_aware=True)
        self.assertEqual(pytz.UTC, stop_watch.start_datetime.tzinfo)


class StopDateTimeTests(unittest.TestCase):
    def test_type(self):
        stop_watch = StopWatch(auto_start=True)
        stop_watch.end()
        self.assertTrue(isinstance(stop_watch.stop_datetime, datetime))

    def test_tz_unaware_local(self):
        stop_watch = StopWatch(auto_start=True)
        stop_watch.end()
        self.assertIsNone(stop_watch.stop_datetime.tzinfo)

    def test_tz_unaware_utc(self):
        stop_watch = StopWatch(auto_start=True, use_utc=True)
        stop_watch.end()
        self.assertIsNone(stop_watch.stop_datetime.tzinfo)

    def test_tz_aware_local(self):
        stop_watch = StopWatch(auto_start=True, make_tz_aware=True)
        stop_watch.end()
        # Since I don`t where this test is going to run, not going to validate the content of tzinfo.
        self.assertIsNotNone(stop_watch.stop_datetime.tzinfo)

    def test_tz_aware_utc(self):
        stop_watch = StopWatch(auto_start=True, use_utc=True, make_tz_aware=True)
        stop_watch.end()
        self.assertEqual(pytz.UTC, stop_watch.stop_datetime.tzinfo)

    def test_end_repeated_call(self):
        stop_watch = StopWatch(auto_start=True)
        expected_elapsed_time = stop_watch.end()
        repeated_elapsed_time = stop_watch.end()
        self.assertEqual(expected_elapsed_time, repeated_elapsed_time)
        

if __name__ == '__main__':
    unittest.main()
