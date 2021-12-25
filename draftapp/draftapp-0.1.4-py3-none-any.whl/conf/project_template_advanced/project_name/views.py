# -*- coding: utf-8 -*-
"""Module for app backend views"""
from flasgger import swag_from
from flask.views import MethodView


class PingView(MethodView):
    """Class for User"""

    # pylint: disable=no-self-use
    @swag_from("swag/ping.yaml")
    def get(self):
        """Get method to get the details of user"""
        return "pong"
