# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inxi']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.8.0,<6.0.0',
 'py-cpuinfo>=8.0.0,<9.0.0',
 'rich>=10.16.1,<11.0.0',
 'typer>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'inxi',
    'version': '0.1.0',
    'description': 'A Python template project',
    'long_description': None,
    'author': 'Jan Willems',
    'author_email': 'jw@elevenbits.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
