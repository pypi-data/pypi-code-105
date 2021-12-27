# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crypto_address_validator', 'crypto_address_validator.validators']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0', 'bech32>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'crypto-address-validator',
    'version': '0.3.1',
    'description': 'Simple validation tool for Bitcoin and other altcoin addresses.',
    'long_description': None,
    'author': 'null-po1nter',
    'author_email': 'me.nullptr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
