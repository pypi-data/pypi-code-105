# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_retention']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'click>=8.0.3,<9.0.0']

setup_kwargs = {
    'name': 'file-retention',
    'version': '0.2.0',
    'description': 'Delete files based on predefined dates',
    'long_description': None,
    'author': 'Gabriel de Mello Barbosa',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
