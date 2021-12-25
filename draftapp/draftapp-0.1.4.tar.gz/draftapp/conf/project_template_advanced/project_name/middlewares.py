# -*- coding: utf-8 -*-
"""Middlewares module in the application"""

from .log import debug


# pylint: disable=unnecessary-pass
@debug
def authentication():
    """Authentication middleware"""
    pass

# pylint: disable=unnecessary-pass
@debug
def authorization():
    """Authorization middleware"""
    pass

# pylint: disable=unnecessary-pass
@debug
def response_middleware():
    """Middlewares for response"""
    pass

# pylint: disable=unnecessary-pass
@debug
def cors_middleware():
    """Middlewares for cors"""
    pass

# pylint: disable=unnecessary-pass
@debug
def request_middleware():
    """Middlewares for request"""
    pass
