# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['congenial_pogato']

package_data = \
{'': ['*']}

install_requires = \
['pandas', 'psycopg2-binary>=2.8.6,<3.0.0']

setup_kwargs = {
    'name': 'congenial-pogato',
    'version': '0.0.1a0',
    'description': 'Convenience wrapper psycopg',
    'long_description': None,
    'author': 'Andrew Rainboldt',
    'author_email': 'arainboldt@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
