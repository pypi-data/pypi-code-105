# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongars']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.42.0,<4.0.0']

entry_points = \
{'console_scripts': ['mongars = mongars.cli:main']}

setup_kwargs = {
    'name': 'mongars',
    'version': '0.1.3',
    'description': 'Show unread emails in INBOX using Gnome Online Accounts',
    'long_description': None,
    'author': 'Chmouel Boudjnah',
    'author_email': 'chmouel@chmouel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
