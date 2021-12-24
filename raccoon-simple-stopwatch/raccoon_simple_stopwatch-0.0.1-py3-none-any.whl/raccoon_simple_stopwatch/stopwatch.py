# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta, timezone
from timeit import default_timer as timer
from typing import Union

import pytz


class StopWatch(object):
    _started_at: Union[datetime, None] = None
    _stopped_at: Union[datetime, None] = None
    _start_timer: Union[timer, None] = None
    _end_timer: Union[timer, None] = None
    _use_utc: bool = False
    _make_tz_aware: bool = False

    """ StopWatch

    A class that manages a StopWatch, so you can easily measure elapsed time of operations.


    Methods
    -------
    start() -> None:
        Starts the timer.

    elapsed(raw: bool = False) -> Union[str, timedelta, None]:
        Returns the current elapsed time.

    end(raw: bool = False) -> Union[str, timedelta, None]:
        Stops the timer and returns the total elapsed time.

    """

    def __init__(self, auto_start: bool = False, use_utc: bool = False, make_tz_aware: bool = False) -> None:
        """
        Creates a new instance of this Stopwatch.

        :param auto_start: if true, will auto start the timer. (Default: False)
        :param use_utc: if true, will get current datetime from utcnow instead of now. (Default: False)
        :param make_tz_aware: if true, will make the datetime objects 'timezone aware'. (Default: False)
        :return: None
        """
        self._use_utc = use_utc
        self._make_tz_aware = make_tz_aware

        if auto_start:
            self.start()

    def _current_timestamp(self) -> datetime:
        """
        Returns the current datetime. It can be local or utc and timezone aware or not, depending on configuration.
        :return: current datetime
        """
        timestamp = datetime.utcnow() if self._use_utc else datetime.now()

        if self._make_tz_aware:
            tz = pytz.utc if self._use_utc else datetime.now(timezone.utc).astimezone().tzinfo
            timestamp = timestamp.replace(tzinfo=tz)

        return timestamp

    @property
    def start_datetime(self) -> datetime:
        """When this timer started"""
        return self._started_at

    @property
    def stop_datetime(self) -> datetime:
        """When this timer stopped"""
        return self._stopped_at

    def start(self) -> None:
        """
        Starts the timer.
        :return: None
        """
        self._started_at = self._current_timestamp()
        self._start_timer = timer()

    def elapsed(self, raw: bool = False) -> Union[str, timedelta, None]:
        """
        Returns the elapsed time either from a current running timer or the total timer,
        if it has been stopped.

        :param raw: if true, will return a timedelta object with the elapsed time.
                    otherwise, will return the string version (days.hours:minutes:seconds.ms)

        :return: elapsed time either in a string or timedelta format.
                 if this method is called before starting the timer, will return None.
        """
        if self._start_timer is None:
            return None

        end = timer() if self._end_timer is None else self._end_timer
        elapsed_time = timedelta(seconds=end - self._start_timer)

        if raw:
            return elapsed_time
        return str(elapsed_time)

    def end(self, raw: bool = False) -> Union[str, timedelta, None]:
        """
        Stops the current timer.
        If it's called multiple times, after the first call, this method will just
        return the elapsed time. (Same behaviour has elasped() method)

        :param raw: if true, will return a timedelta object with the elapsed time.
                    otherwise, will return the string version (days.hours:minutes:seconds.ms)

        :return: elapsed time either in a string or timedelta format.
        """
        if self._end_timer is not None:
            return self.elapsed(raw=raw)

        self._stopped_at = self._current_timestamp()
        self._end_timer = timer()

        return self.elapsed(raw=raw)


if __name__ == '__main__':
    sw = StopWatch()
    print(sw.start_datetime)
    sw.start()
    print(f"{sw.start_datetime} | {sw.start_datetime.tzinfo}")
    sw2 = StopWatch(use_utc=True)
    print(sw2.start_datetime)
    sw2.start()
    print(f"{sw2.start_datetime} | {sw2.start_datetime.tzinfo}")
