# -*- coding: utf-8 -*-
"""config file for app"""
import configparser
import os

# pylint: disable=invalid-name
config_file = os.getenv("SETTINGS", "/project_name/configs/local.ini")


# define config parser
config = configparser.ConfigParser(allow_no_value=True)
config.read(config_file)
