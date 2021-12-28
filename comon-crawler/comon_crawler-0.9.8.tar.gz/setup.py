# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comon_crawler']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.17.0,<0.18.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'comon-crawler',
    'version': '0.9.8',
    'description': '',
    'long_description': None,
    'author': 'roci',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
