# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acenus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'acenus',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'tsarbas',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
