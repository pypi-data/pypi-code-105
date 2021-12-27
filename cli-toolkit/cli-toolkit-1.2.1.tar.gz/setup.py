# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli_toolkit', 'cli_toolkit.tests']

package_data = \
{'': ['*']}

install_requires = \
['setproctitle>=1.2,<2.0', 'sys-toolkit>=1.2,<2.0']

entry_points = \
{'pytest11': ['cli_toolkit_fixtures = cli_toolkit.fixtures']}

setup_kwargs = {
    'name': 'cli-toolkit',
    'version': '1.2.1',
    'description': 'Classes to implement CLI commands in python',
    'long_description': None,
    'author': 'Ilkka Tuohela',
    'author_email': 'hile@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
