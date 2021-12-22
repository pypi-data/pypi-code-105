import os
import uuid
from datetime import date
from decimal import Decimal
from logging.config import dictConfig

from flask import Flask, make_response, jsonify
from flask import request, g
from flask.json import JSONEncoder
from flask_restful import Resource
from . import ProjectXApi
from .exception import GenericException
from ..util.logger import BASIC_CONFIG
from .utils import get_flask_env
from time import time


def handle_web_exception(e: GenericException):
    return handle_web_exception_from_message_and_code(e.message, e.http_code)


def handle_web_exception_from_message_and_code(message, code):
    return make_response(jsonify({'message': message, 'code': code}), code)


def create_app(flask_routes=None):
    app = Flask(__name__)
    app.config.from_object(f'flaskr.settings.common')
    app.config.from_object(f'flaskr.settings.{get_flask_env(default="dev")}')

    # override configuration with environment vars
    app.config.from_mapping({k: v for k, v in dict(os.environ).items() if k in dict(app.config)})

    with app.app_context() as context:
        dictConfig(BASIC_CONFIG())

    app.logger.info({'type': 'start_app'})

    if flask_routes:
        for flask_route in flask_routes:
            flask_route['rule'] = app.config['APPLICATION_ROOT'] + flask_route['rule']
            app.add_url_rule(**flask_route)

    api = ProjectXApi(app, catch_all_404s=True, prefix=app.config['APPLICATION_ROOT'])

    if app.config.get('JSON_ENCODER', None):
        app.json_encoder = app.config['JSON_ENCODER']

    api.add_resource(HealthCheckResource, '/health')

    @app.before_request
    def before():
        g.request_id = uuid.uuid4().hex
        if 'User' in request.headers:
            g.user = request.headers['User']
        g.start_time = time()
        request_log = {
            'type': 'request_started',
            'full_path': request.full_path,
            'path': request.path,
            'args': {
                key: value if len(value) > 1 else value[0]
                for key, value in request.args.to_dict(flat=False).items()
            },
            'headers': dict(request.headers)
        }
        app.logger.info(request_log)

    @app.after_request
    def after(response):
        time_executed = time() - g.start_time
        request_log = {
            'type': 'request_finished',
            'full_path': request.full_path,
            'path': request.path,
            'headers': dict(response.headers),
            'execution_time_seconds': time_executed,
            'status_code': response.status_code,
        }
        app.logger.info(request_log)
        return response

    return app, api


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)


class HealthCheckResource(Resource):

    def get(self):
        return jsonify(success=True)
