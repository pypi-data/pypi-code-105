# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_gandi_dns_dynip']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26,<3.0']

entry_points = \
{'console_scripts': ['gandi-dns-dynip = py_gandi_dns_dynip.main:main']}

setup_kwargs = {
    'name': 'py-gandi-dns-dynip',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Nicolas Olivier',
    'author_email': 'nico@kingtong.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
