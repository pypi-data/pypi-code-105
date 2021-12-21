#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

import logging
import logging.handlers
import logging.config
import os
from vcli.constant import LOG_LEVEL, LOG_FILE


LOG_CONFIG_PATH = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'logging.conf')


class Logger:
    def __init__(self):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    def get_logger(self) -> logging.Logger:
        logging.config.fileConfig(
            LOG_CONFIG_PATH, disable_existing_loggers=True)
        if LOG_LEVEL.lower() == 'debug':
            logger = logging.getLogger('debug')
        else:
            logger = logging.getLogger('default')
        return logger


if "LOGGER" not in globals():
    logger = Logger().get_logger()
