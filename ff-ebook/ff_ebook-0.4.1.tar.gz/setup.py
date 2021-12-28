# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ff_ebook']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'cloudscraper>=1.2.58,<2.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'ff-ebook',
    'version': '0.4.1',
    'description': 'Ebook generator for fanfiction sites.',
    'long_description': None,
    'author': 'Neia Neutuladh, Michal Hozza',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
