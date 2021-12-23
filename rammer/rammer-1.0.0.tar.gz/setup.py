# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rammer']
setup_kwargs = {
    'name': 'rammer',
    'version': '1.0.0',
    'description': 'Make a RAM indicator \\ print in your python code!',
    'long_description': None,
    'author': 'OwoNicoo',
    'author_email': '86409467+DiscordBotML@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
