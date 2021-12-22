# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsfy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tsfy',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Xiaocong Sun',
    'author_email': 'xiaocong.sun@unianalysis.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
