"""
Module used for timing process with the TimeMeasure class.
"""

import os
import time
import sys
from typing import Callable
from datetime import date, datetime, timedelta
import logging
import json


def timer_function(func: Callable) -> None:
    """
    Decorator function calculates the time it took function func to finish, result is printed out.

    Args:
        func (Callable): Callable of type function.
    """
    def wrap_func(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'# Function: {func.__name__!r} executed in {(end_time - start_time):.4f}s')
        return result
    return wrap_func


class TimeMeasure:
    """
    Class for measuring time.

    A logging function can be passed for saving start / end data.
    """
    def __init__(self, logging_function: Callable = print):
        """
        Args:
            logging_function: A logging function used system wide to save to log files. Defaults to print.
        """
        self.start_time = 0
        self.end_time = 0
        self._elapsed_seconds = 0

        self.logging_function = logging_function

    @property
    def elapsed_seconds(self) -> float:
        if self.end_time == 0:  # Has not yet been set
            self._elapsed_seconds = datetime.now().timestamp() - self.start_time
        else:
            self._elapsed_seconds = self.end_time - self.start_time
        return round(self._elapsed_seconds, 2)

    @elapsed_seconds.setter
    def elapsed_seconds(self, elapsed_sec):
        self._elapsed_seconds = elapsed_sec

    def start(self) -> float:
        """
        Methods starts the time measure while also logging it with the passed logging_function.

        Returns:
            float: Unix timestamp at start of measuring.
        """
        self.logging_function("Time measure: Started.")
        self.start_time = datetime.now().timestamp()
        return self.start_time

    def stop(self) -> int:
        """
        Method stops the time measure and outputs the elapsed time, also returning the elapsed seconds.

        Returns:
            int: Elapsed time in seconds.
        """
        self.end_time = datetime.now().timestamp()
        self.elapsed_seconds = int(self.end_time - self.start_time)
        self.logging_function(
            f"Time measure: Ended, total time: {TimeMeasure.seconds_to_time_string(self.elapsed_seconds)}."
        )
        return self.elapsed_seconds

    @staticmethod
    def current_time_date() -> str:
        """
        Method returns a string of the current time date in the format dd-mm-yyyy_hh-mm-ss

        Returns:
            str: Current time date string in above format.
        """
        return date.today().strftime("%d-%m-%Y_%H-%M-%S")

    @staticmethod
    def current_time() -> str:
        """
        Method returns a string of the current time in the format hh:mm:ss

        Returns:
            str: Current time in above format
        """
        return date.today().strftime("%H:%M:%S")

    @staticmethod
    def seconds_to_time_string(seconds) -> str:
        """
        Method converts seconds into time in the format hh:mm:ss. Returns a string

        Returns:
            str: Time in the format hh:mm:ss
        """
        return str(timedelta(seconds=seconds)).split(".")[0]  # Chop off microseconds/milliseconds

    def __str__(self) -> str:
        return str(datetime.timedelta(seconds=self.elapsed_seconds))

    def __repr__(self) -> str:
        return f"<TimeMeasure: elapsed = {self.__str__()}>"
