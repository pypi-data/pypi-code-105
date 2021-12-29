#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging.config


# _formatter = logging.Formatter('logging_time: %(asctime)s - logging_level: %(levelname)s - logging_message: %(message)s'
#                                '- program_pid: %(process)d')
#
# main_logger = logging.getLogger('main_logger')
#
# # 设置全局级别
# main_logger.setLevel(logging.INFO)
#
# # 创建控制台处理器
# console_handler = logging.StreamHandler(sys.stdout)
#
# # 设置控制台等级
# console_handler.setLevel(logging.INFO)
#
# # 给处理器设置输出格式
# console_handler.setFormatter(_formatter)
#
# # 日志器添加处理器
# main_logger.addHandler(console_handler)

config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "logging_time: %(asctime)s - logging_level: %(levelname)s - logging_message: %(message)s "
                      "- program_pid: %(process)d"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
    },
    "loggers": {
        "main_logger": {
            "level": "INFO",
            "handlers": ["console"]
        }
    }
}

logging.config.dictConfig(config)
