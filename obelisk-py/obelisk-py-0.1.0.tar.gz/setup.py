# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obelisk']

package_data = \
{'': ['*']}

install_requires = \
['Rx>=1.6.1,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'sgqlc>=14.1,<15.0',
 'sseclient-py>=1.7,<2.0']

setup_kwargs = {
    'name': 'obelisk-py',
    'version': '0.1.0',
    'description': 'Python client for the Obelisk API (v3)',
    'long_description': '# Obelisk Python Client\n\n![build-docs](https://img.shields.io/github/workflow/status/predict-idlab/obelisk-python/pages%20build%20and%20deployment?label=docs)\n\n## Installation\n\n## Documentation\n\n[Read the docs](https://predict-idlab.github.io/obelisk-python/)',
    'author': 'Pieter Moens',
    'author_email': 'pieter.moens@ugent.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/predict-idlab/obelisk-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
