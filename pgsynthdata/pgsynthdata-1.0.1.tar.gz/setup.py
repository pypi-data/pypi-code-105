# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgsynthdata', 'pgsynthdata.generators', 'pgsynthdata.generators.legacy']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=9.8.0,<10.0.0',
 'click>=8.0.1,<9.0.0',
 'numpy>=1.21.2,<2.0.0',
 'prettytable>=2.4.0,<3.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'radar>=0.3,<0.4',
 'toposort>=1.7,<2.0']

setup_kwargs = {
    'name': 'pgsynthdata',
    'version': '1.0.1',
    'description': 'Synthetic Data Generator for PostgreSQL',
    'long_description': None,
    'author': 'Timon Erhart',
    'author_email': 'timon.erhart@ost.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
