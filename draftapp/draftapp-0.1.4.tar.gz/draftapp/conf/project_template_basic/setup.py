# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="project_name",
    version="1.0.0",
    description="App Backend",
    classifiers=["Programming Language :: Python :: 3.6.9"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flasgger==0.9.3",
        "flask==1.1.1",
        "flask-cors==3.0.8",
        "gunicorn==19.9.0",
        "marshmallow==2.19.5",
        "pyjwt==1.7.1",
        "sqlalchemy==1.3.5",
        "pylint==2.4.4",
        "Cython==0.29.15",
        "Flask-SQLAlchemy==2.4.4",
        "psycopg2-binary",
        "Flask-Migrate==2.5.2",
        "alembic==1.0.11",
        "black",
        "requests",
    ],
    scripts=["bin/project_name-cli"],
)
