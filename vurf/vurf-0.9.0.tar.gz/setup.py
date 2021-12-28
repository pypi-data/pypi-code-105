# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vurf']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0,<9.0.0', 'lark>=0.11.3,<0.12.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['vurf = vurf.cli:main']}

setup_kwargs = {
    'name': 'vurf',
    'version': '0.9.0',
    'description': '',
    'long_description': None,
    'author': 'Viliam Valent',
    'author_email': 'vurf@valent.email',
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
