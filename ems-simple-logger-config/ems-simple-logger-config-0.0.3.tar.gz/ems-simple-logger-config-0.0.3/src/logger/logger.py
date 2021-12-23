"""
Simple logger configuration
"""
import logging
import sys

LOGGER_NAME = 'Logger'

def setup_logger(
        logger_name = LOGGER_NAME,
        log_level=logging.DEBUG,
        file_name=None):
    """
    Setup application top logger

    Args:
        logger_name (string, optional): Name of the logger. Defaults to LOGGER_NAME.
            Default value 'Logger'
        level (Logging level, optional): Logging level. Defaults to logging.DEBUG.
        file_name (string, optional): Optional log file. Defaults to None.
            A file logger is created if file name is given

    Returns:
        Logger: Application top logger
    """

    logger = logging.getLogger(logger_name)

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(stream_handler)

    if file_name:
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(module_name):
    """
    Returns logger for the given module name

    Args:
        module_name (string): Name of the module

    Returns:
        Logger: Logger for the given module name
    """
    return logging.getLogger(LOGGER_NAME).getChild(module_name)
