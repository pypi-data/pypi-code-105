"""
Module for the logging system of saving processes.
"""

import os
from datetime import date, datetime
import logging
import json
import os


# Make global variables at import time
current_date = date.today().strftime("%d-%m-%Y")
current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
save_folder = "logs"
log_filename = os.path.join(save_folder, current_time + ".log")


def logger_setup(
    save_folder_path: str,
    filename: str = None,
    filemode: str = 'a',
    format: str = '%(asctime)s - %(message)s',
    level: int = logging.INFO,
    datefmt: str = '%d-%m-%y %H:%M:%S'
):
    """
    Setup for logging. This function should be called from the main thread before other threads are started.

    After setting the base directory, logger will will create a folder for every date called,
    and files will be saved in that folder with names of the current time.

    Args:
        save_folder_path: Base folder path of where to save the logging files to.
        Arguments passed to the logging.basicConfig:
        filename: Defaults to current time in the format d-m-y_H-M-S.
        filemode: Defaults to 'a'.
        format: Defaults to '%(asctime)s - %(message)s'.
        level: Defaults to logging.INFO.
        datefmt: Defaults to '%d-%m-%y %H:%M:%S'.
    """

    current_date = date.today().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    save_folder = os.path.join(save_folder_path, current_date)
    if not os.path.isdir(save_folder):
        os.mkdir(save_folder)  # Create directory

    log_filename = os.path.join(save_folder, current_time + ".log")
    if not filename:
        filename = log_filename
    logging.basicConfig(
        filename=filename,
        filemode=filemode,
        format=format,
        level=level,
        datefmt=datefmt)


class Logger:
    """
    Class for logging info into the .log file  based on settings passed by the logger setup.
    Methods also print to the standard output.
    """
    current_save_folder_path = save_folder

    @staticmethod
    def log(log_entry: str, out_print: bool = True, indent: int = 0) -> None:
        """
        logging function for saving logs to the log file and printing to console.

        Args:
            log_entry: String to be logged and printed(if set)
            out_print: If log should be printed to the console. Defaults to True.
            indent: How many indents(4 spaces) should be put in front of the string to output.
        """
        logging.info(log_entry)
        if out_print:
            if indent == 0:
                print(log_entry)
            else:
                print((indent * 4) * " " + log_entry)

    @staticmethod
    def log_dict(log_entry: dict, entry_name: str = "Dictionary") -> None:
        """
        logging function for saving logs of dictionaries to the log file and pretty printing to standard output.

        Args:
            log_entry: Dictionary to be pretty printed.
            entry_name: Name of dictionary.
        """
        logging.info(log_entry)
        print(entry_name, end=": ")
        print(json.dumps(log_entry, indent=4, sort_keys=False))
