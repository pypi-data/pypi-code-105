# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tokens_example',
 'tokens_example.core',
 'tokens_example.tokens',
 'tokens_example.tokens.management',
 'tokens_example.tokens.management.commands',
 'tokens_example.tokens.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3,<4']

setup_kwargs = {
    'name': 'django-verification-example',
    'version': '0.1.0',
    'description': 'A project that includes an application that demonstrates how you can organize work with security tokens.',
    'long_description': None,
    'author': 'Michael Might',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mikemight/django-tokens-example/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
