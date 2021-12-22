import os

from flask import request


def get_flask_env(default='test'):
    return os.environ['FLASK_ENV'] if 'FLASK_ENV' in os.environ else default


def accept_is_csv():
    return request.headers['Accept'] == 'text/csv'
