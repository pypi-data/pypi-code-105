# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poem_fa', 'poem_fa.hafez']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poem-fa',
    'version': '0.1.0',
    'description': 'A python package for persian poems',
    'long_description': None,
    'author': 'Mehdi Ghodsizadeh',
    'author_email': 'mehdi.ghodsizadeh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
