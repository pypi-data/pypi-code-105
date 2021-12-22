# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_isolated_packages']
install_requires = \
['astpretty>=2.1.0,<3.0.0', 'flake8>=4,<5']

setup_kwargs = {
    'name': 'flake8-isolated-packages',
    'version': '1.0.0',
    'description': 'This Flake8 plugin is for checking imports isolations.',
    'long_description': None,
    'author': 'Dudov Dmitry',
    'author_email': 'dudov.dm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
