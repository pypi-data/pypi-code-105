"""File that contains exception class used in the package avalonBG"""


class AvalonBGError(Exception):
    """Class AvalonBGError related to specific exception"""

    def __init__(self, msg, log_type="error"):
        Exception.__init__(self, msg)
