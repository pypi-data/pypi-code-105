# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djbookshelf', 'djbookshelf.migrations', 'djbookshelf.models']

package_data = \
{'': ['*'], 'djbookshelf': ['templates/djbookshelf/*']}

install_requires = \
['django-bootstrap-v5>=1.0.7,<2.0.0',
 'django>=3.2,<5',
 'isbnlib>=3.10.9,<4.0.0',
 'requests>=2,<3']

setup_kwargs = {
    'name': 'djbookshelf',
    'version': '0.1.4',
    'description': '',
    'long_description': '# DjBookShelf\n\nThis is a Django module for manage books\n\nYou can find the [documentation here](https://djbookshelf.readthedocs.io/en/latest/)\n',
    'author': 'Fundor333',
    'author_email': 'fundor333@fundor333.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://djbookshelf.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
