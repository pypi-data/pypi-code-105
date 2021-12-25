# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eph_py']

package_data = \
{'': ['*'], 'eph_py': ['csv_data/*']}

install_requires = \
['pandas>=1.3.5,<2.0.0',
 'pyreadr>=0.4.4,<0.5.0',
 'requests>=2.26.0,<3.0.0',
 'wget>=3.2,<4.0']

setup_kwargs = {
    'name': 'eph-py',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
