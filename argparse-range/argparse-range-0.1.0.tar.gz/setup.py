# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argparse_range']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'argparse-range',
    'version': '0.1.0',
    'description': 'Numeric range for argparse arguments',
    'long_description': None,
    'author': 'Aatif Syed',
    'author_email': 'aatifsyedyp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aatifsyed/argparse-range',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
