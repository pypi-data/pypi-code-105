# -*- coding: utf-8 -*-
"""Module for Database Models"""
from uuid import uuid4
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


# pylint: disable=too-few-public-methods
class ModelMixin:
    """Base table for application"""

    id = sa.Column(sa.String(100), primary_key=True, default=str(uuid4()))

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if getattr(self, key):
                setattr(self, key, val)
