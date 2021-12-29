# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmdline']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cmdline-mini',
    'version': '1.0.1',
    'description': 'Partial command line handler',
    'long_description': None,
    'author': 'David Nugent',
    'author_email': 'david.nugent@news.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
