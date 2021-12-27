# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['blueskyapi']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1,<2.0', 'requests>=2.0,<3.0']

setup_kwargs = {
    'name': 'blueskyapi',
    'version': '0.1.0a1',
    'description': 'Client for blueskyapi.io',
    'long_description': '# python-client\nPython client for blueskyapi.io\n',
    'author': 'blueskyapi.io',
    'author_email': 'contact@blueskyapi.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://blueskyapi.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
