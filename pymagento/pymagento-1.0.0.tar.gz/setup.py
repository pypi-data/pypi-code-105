# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magento']

package_data = \
{'': ['*']}

install_requires = \
['api-session>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'pymagento',
    'version': '1.0.0',
    'description': 'Python client for the Magento 2 API',
    'long_description': None,
    'author': 'Bixoto',
    'author_email': 'info@bixoto.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Bixoto/PyMagento',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
