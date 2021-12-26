#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Ahmet KÖKEN
# Email       : ahmetkkn07@gmail.com
# GitHub      : https://github.com/ahmetkkn07
# =============================================================================
"""Colored custom logger module by ahmetkkn07 (Python3.6+ Compatible)"""
# =============================================================================
# Imports
# =============================================================================
import os
import datetime
import inspect


class LogLevel:
    FATAL = 900
    ERROR = 800
    WARNING = 700
    INFO = 600
    DEBUG = 500
    TRACE = 400
    TEST = 300
    ALL = 100


class Term:
    BOLD = '\033[1m'
    REVERSE = "\033[;7m"
    CLEAR = '\033[0m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    # unused
    CYAN = '\033[96m'


class Alogger:
    def __init__(
        self,
        path="",
        log_level=LogLevel.ALL,
        log_to_file=True,
        log_name=None,
        log_file_type="txt"
    ) -> None:
        """Constructor of Alogger class.

        Args:
            log_level (LogLevel, optional): Set level to log. Defaults to ALL
            log_to_file (bool, optional): Set True if you want to save logs
                to file. Defaults to False.
            log_name (str, optional): Custom file name for log file.
                Defaults to caller filename.
            log_file_type (str, optional): Type of file that saved logs.
                Defaults to 'txt', can set to 'html'.
        """
        self.log_level = log_level
        self.log_to_file = log_to_file
        self.log_file_type = log_file_type
        self.caller_filename = f"{inspect.stack()[1].filename.split('.py')[0]}"
        if os.name == "nt":
            self.caller_filename = self.caller_filename.split("\\")[-1]
        elif os.name == "posix":
            self.caller_filename = self.caller_filename.split("/")[-1]
        if path != "":
            self.path = path
        else:
            self.path = os.curdir
        if log_to_file:
            if log_name is not None:
                self.log_name = log_name
            else:
                if log_file_type == "html":
                    self.log_name = f"{self.caller_filename}_log.html"
                    if os.name == "nt":
                        self.log_name = self.log_name.split("\\")[-1]
                    elif os.name == "posix":
                        self.log_name = self.log_name.split("/")[-1]
                elif log_file_type == "txt":
                    self.log_name = f"{self.caller_filename}.log"
                    if os.name == "nt":
                        self.log_name = self.log_name.split("\\")[-1]
                    elif os.name == "posix":
                        self.log_name = self.log_name.split("/")[-1]

    def fatal(self, *messages) -> None:
        if self.log_level <= LogLevel.FATAL:
            caller = inspect.stack()[1]  # 0 represents this line
            frame = caller[0]
            info = inspect.getframeinfo(frame)
            caller = f"@{self.caller_filename}.{inspect.stack()[1][3]}:"\
                + f"{info.lineno}"
            caller = caller.replace("<module>", "_")
            messages = [str(message) for message in messages]
            print(
                f"{Term.REVERSE}{Term.RED}FATAL: {' '.join(messages)}. "
                + f"{caller}{Term.CLEAR}")
            message = self._create_message(messages, caller, "FATAL")
            self._write_to_file(message)

    def error(self, *messages) -> None:
        if self.log_level <= LogLevel.ERROR:
            caller = inspect.stack()[1]  # 0 represents this line
            frame = caller[0]
            info = inspect.getframeinfo(frame)
            caller = f"@{self.caller_filename}.{inspect.stack()[1][3]}:"\
                + f"{info.lineno}"
            caller = caller.replace("<module>", "_")
            messages = [str(message) for message in messages]
            print(
                f"{Term.RED}{Term.BOLD}ERROR: {' '.join(messages)}. "
                + f"{caller}{Term.CLEAR}")
            message = self._create_message(messages, caller, "ERROR")
            self._write_to_file(message)

    def warning(self, *messages) -> None:
        if self.log_level <= LogLevel.WARNING:
            caller = inspect.stack()[1]  # 0 represents this line
            frame = caller[0]
            info = inspect.getframeinfo(frame)
            caller = f"@{self.caller_filename}.{inspect.stack()[1][3]}:"\
                + f"{info.lineno}"
            caller = caller.replace("<module>", "_")
            messages = [str(message) for message in messages]
            print(
                f"{Term.YELLOW}{Term.BOLD}WARNING: {' '.join(messages)}. "
                + f"{caller}{Term.CLEAR}")
            message = self._create_message(messages, caller, "WARNING")
            self._write_to_file(message)

    def info(self, *messages) -> None:
        if self.log_level <= LogLevel.INFO:
            caller = inspect.stack()[1]  # 0 represents this line
            frame = caller[0]
            info = inspect.getframeinfo(frame)
            caller = f"@{self.caller_filename}.{inspect.stack()[1][3]}:"\
                + f"{info.lineno}"
            caller = caller.replace("<module>", "_")
            messages = [str(message) for message in messages]
            print(
                f"{Term.GREEN}{Term.BOLD}INFO: {' '.join(messages)}. "
                + f"{caller}{Term.CLEAR}")
            message = self._create_message(messages, caller, "INFO")
            self._write_to_file(message)

    def debug(self, *messages) -> None:
        if self.log_level <= LogLevel.DEBUG:
            caller = inspect.stack()[1]  # 0 represents this line
            frame = caller[0]
            info = inspect.getframeinfo(frame)
            caller = f"@{self.caller_filename}.{inspect.stack()[1][3]}:"\
                + f"{info.lineno}"
            caller = caller.replace("<module>", "_")
            messages = [str(message) for message in messages]
            print(
                f"{Term.BLUE}{Term.BOLD}DEBUG: {' '.join(messages)}. "
                + f"{caller}{Term.CLEAR}")
            message = self._create_message(messages, caller, "DEBUG")
            self._write_to_file(message)

    def trace(self, *messages) -> None:
        if self.log_level <= LogLevel.TRACE:
            caller = inspect.stack()[1]  # 0 represents this line
            frame = caller[0]
            info = inspect.getframeinfo(frame)
            caller = f"@{self.caller_filename}.{inspect.stack()[1][3]}:"\
                + f"{info.lineno}"
            caller = caller.replace("<module>", "_")
            messages = [str(message) for message in messages]
            print(
                f"{Term.PURPLE}{Term.BOLD}TRACE: {' '.join(messages)}. "
                + f"{caller}{Term.CLEAR}")
            message = self._create_message(messages, caller, "TRACE")
            self._write_to_file(message)

    def test(self, *messages) -> None:
        if self.log_level <= LogLevel.TEST:
            caller = inspect.stack()[1]  # 0 represents this line
            frame = caller[0]
            info = inspect.getframeinfo(frame)
            caller = f"@{self.caller_filename}.{inspect.stack()[1][3]}:"\
                + f"{info.lineno}"
            caller = caller.replace("<module>", "_")
            messages = [str(message) for message in messages]
            print(
                f"{Term.REVERSE}{Term.BOLD}TEST: {' '.join(messages)}. "
                + f"{caller}{Term.CLEAR}")
            message = self._create_message(messages, caller, "TEST")
            self._write_to_file(message)

    def _write_to_file(self, message: str):
        if self.log_to_file:
            os.chdir(self.path)
            with open(self.log_name, "a+") as file:
                file.write(f"{message}\n\n")

    def _create_message(self, messages, caller, log_type):
        now = datetime.datetime.now()
        message = ""
        if self.log_file_type == "html":
            message = '<div style="background-color:#FF5C57; '\
                + f'color: #282A36;">{now} {log_type}: {" ".join(messages)}. '\
                + f'{caller} < /div >'
        elif self.log_file_type == "txt":
            message = f'{now} {log_type}: {" ".join(messages)}. {caller}'
        return message
