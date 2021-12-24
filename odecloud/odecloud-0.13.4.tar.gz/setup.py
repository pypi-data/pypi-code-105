# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odecloud', 'odecloud.api']

package_data = \
{'': ['*']}

install_requires = \
['certifi==2021.10.8',
 'charset-normalizer==2.0.9',
 'idna==3.3',
 'requests==2.26.0',
 'urllib3==1.26.7']

setup_kwargs = {
    'name': 'odecloud',
    'version': '0.13.4',
    'description': '',
    'long_description': None,
    'author': 'Vanielle Lee',
    'author_email': 'vanielle@odecloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
