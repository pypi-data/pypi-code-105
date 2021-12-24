# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jitb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jitb',
    'version': '0.1.0',
    'description': 'A small library containing some utilities to jump-scare you',
    'long_description': None,
    'author': 'Binyamin Y Cohen',
    'author_email': 'binyamincohen555@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
