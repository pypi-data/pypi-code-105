# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shared_dependencies']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'httpx>=0.21.1,<0.22.0', 'sentry-sdk>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'shared-dependencies',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jean-Charles Bouchaud',
    'author_email': 'jeancharles-b@evidenceb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
