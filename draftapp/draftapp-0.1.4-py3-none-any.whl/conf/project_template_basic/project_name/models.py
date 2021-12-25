# -*- coding: utf-8 -*-
"""Module for database Models"""
import sqlalchemy as sa
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ModelMixin:
    """Base table for application"""

    id = sa.Column(sa.String(100), primary_key=True, default=str(uuid4()))

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if getattr(self, key):
                setattr(self, key, val)
