# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['purgatory',
 'purgatory.domain',
 'purgatory.domain.messages',
 'purgatory.service',
 'purgatory.service.handlers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'purgatory-circuitbreaker',
    'version': '0.1.0',
    'description': 'A circuit breaker implementation for asyncio',
    'long_description': 'Purgatory\n=========\n\nA circuit breaker implementation for asyncio.\n',
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gauvr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mardiros/purgatory',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
