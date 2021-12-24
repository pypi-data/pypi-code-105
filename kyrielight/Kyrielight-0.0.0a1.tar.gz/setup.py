# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kyrielight']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kyrielight',
    'version': '0.0.0a1',
    'description': 'A WIP app for some random api.',
    'long_description': None,
    'author': 'mooncell07',
    'author_email': 'mooncell07@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
