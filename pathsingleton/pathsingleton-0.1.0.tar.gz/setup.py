# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pathsingleton']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pathsingleton',
    'version': '0.1.0',
    'description': 'Module to track the directory our program starts in.',
    'long_description': None,
    'author': 'Yashesh Dasari',
    'author_email': 'ydasari@uwaterloo.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
