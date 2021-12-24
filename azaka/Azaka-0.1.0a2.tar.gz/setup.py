# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azaka', 'azaka.commands', 'azaka.connection', 'azaka.objects', 'azaka.tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'azaka',
    'version': '0.1.0a2',
    'description': 'A work in progress API Wrapper around The Visual Novel Database (VNDB) written in Python.',
    'long_description': '',
    'author': 'mooncell07',
    'author_email': 'mooncell07@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
