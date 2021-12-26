# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gamesortvisualize']

package_data = \
{'': ['*']}

install_requires = \
['pygame>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'gamesortvisualize',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'sakthiRatnam',
    'author_email': 'sakthiratnam050@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.5,<4.0.0',
}


setup(**setup_kwargs)
