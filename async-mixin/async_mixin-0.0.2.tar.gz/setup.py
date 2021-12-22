# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_mixin']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'asyncio-throttle>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'async-mixin',
    'version': '0.0.2',
    'description': 'Boilerplate for an Asynchronous HTTP REST Client as a Mixin',
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
