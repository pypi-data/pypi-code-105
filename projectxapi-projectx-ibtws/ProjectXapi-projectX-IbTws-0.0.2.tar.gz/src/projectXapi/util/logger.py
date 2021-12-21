import logging
import os
from logging.handlers import DatagramHandler

from flask import current_app, has_request_context, g
from pythonjsonlogger import jsonlogger


def BASIC_CONFIG():
    logger_level = os.environ['LOGGER_LEVEL'] if 'LOGGER_LEVEL' in os.environ else 'INFO'
    formatter = {
        'class': 'projectXapi.util.logger.RequestFormatter',
        'format': '%(asctime)s [%(levelname)s] %(request_id)s %(user)s %(name)s %(message)s'
    }
    if os.environ.get('JSON_LOGS', '0') == '1':
        formatter = {
            'class': 'projectXapi.util.logger.CustomJsonFormatter',
            'format': '%(asctime)s [%(levelname)s] %(request_id)s %(user)s %(name)s %(type)s %(message)s'
        }
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'stream': formatter,
            'file': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'logstash': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'stream_handler': {
                'level': logger_level,
                'class': 'logging.StreamHandler',
                'formatter': 'stream',
            },
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'stream'
            },
            'logstash_handler': {
                'level': logger_level,
                'class': 'projectXapi.util.logger.LogStashSocketHandler',
                'host': None,
                'port': None,
                'formatter': 'logstash'
            }
        },
        'loggers': {
            'init': {
                'handlers': ['stream_handler', 'logstash_handler'],
                'level': logger_level,
                'propagate': True
            }
        },
        'root': {
            'level': logger_level,
            'handlers': ['wsgi']
        }
    }


class LogStashSocketHandler(DatagramHandler):

    def __init__(self, host=None, port=None):
        self.host = current_app.config['LOGSTASHOST']
        self.port = current_app.config['LOGSTASPORT']
        super().__init__(self.host, self.port)

    def makePickle(self, record):
        return str.encode(self.format(record))


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['request_id'] = None
        log_record['user'] = None
        if has_request_context():
            log_record['request_id'] = g.request_id if 'request_id' in g else None
            log_record['user'] = g.user if 'user' in g else None
        log_record['type'] = 'text'
        if message_dict:
            log_type = message_dict.pop('type', None)
            log_record['type'] = 'normal' if log_type is None else log_type
            for key in message_dict.keys():
                log_record.pop(key)
            log_record['message'] = message_dict


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.request_id = None
        record.user = None
        if has_request_context():
            record.request_id = g.request_id if 'request_id' in g else None
            record.user = g.user if 'user' in g else None
        return super().format(record)