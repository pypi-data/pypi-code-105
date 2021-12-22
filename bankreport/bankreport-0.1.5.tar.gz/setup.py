# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bankreport']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pandas>=1.1.4,<2.0.0']

entry_points = \
{'console_scripts': ['bankreport = bankreport:main']}

setup_kwargs = {
    'name': 'bankreport',
    'version': '0.1.5',
    'description': 'Parse and analyze csv files from online banking.',
    'long_description': None,
    'author': 'Heinrich Hartmann',
    'author_email': 'heinrich@heinrichhartmann.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/heinrichhartmann/bankreport',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
