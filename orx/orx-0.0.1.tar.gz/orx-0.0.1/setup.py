# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orx']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'orx',
    'version': '0.0.1',
    'description': 'A modern, async API wrapper for Discord',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
