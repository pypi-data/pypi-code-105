# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caserunner']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['caserunner = caserunner.caserunner:main']}

setup_kwargs = {
    'name': 'caserunner',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'luweisen',
    'author_email': 'luweisen@sina.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
