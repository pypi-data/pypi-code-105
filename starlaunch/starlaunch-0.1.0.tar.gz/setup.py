# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlaunch']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['starlaunch = starlaunch.starlaunch:main']}

setup_kwargs = {
    'name': 'starlaunch',
    'version': '0.1.0',
    'description': 'A tool to create, configure, and launch isolated Starbound instances.',
    'long_description': None,
    'author': 'Nick Thurmes',
    'author_email': 'nthurmes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
