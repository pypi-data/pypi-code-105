# -*- coding: utf-8 -*-
"""Module for functions"""
from .config import config


def create_db_config(application):
    """creates database configuration"""
    application.config["SQLALCHEMY_DATABASE_URI"] = config.get("database", "url")
    application.config["SQLALCHEMY_ECHO"] = False
    if config.getboolean("testing", "testing"):
        application.config["SQLALCHEMY_POOL_SIZE"] = None
    else:
        application.config["SQLALCHEMY_POOL_SIZE"] = config.getint(
            "database", "pool_size"
        )
    if config.getboolean("testing", "testing"):
        application.config["SQLALCHEMY_POOL_TIMEOUT"] = None
    else:
        application.config["SQLALCHEMY_POOL_TIMEOUT"] = config.getint(
            "database", "pool_timeout"
        )
    application.config["SQLALCHEMY_POOL_RECYCLE"] = config.getint(
        "database", "pool_recycle"
    )
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return application
