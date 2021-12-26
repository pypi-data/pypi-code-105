# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrap']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0.3,<4.0.0', 'numpy>=1.19.1,<2.0.0']

setup_kwargs = {
    'name': 'rrap',
    'version': '0.1.0',
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
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
