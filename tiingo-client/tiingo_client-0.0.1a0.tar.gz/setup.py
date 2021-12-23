# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiingo_client']

package_data = \
{'': ['*']}

install_requires = \
['async-mixin==0.0.2', 'pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'tiingo-client',
    'version': '0.0.1a0',
    'description': '',
    'long_description': None,
    'author': 'Andrew Rainboldt',
    'author_email': 'arainboldt@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
