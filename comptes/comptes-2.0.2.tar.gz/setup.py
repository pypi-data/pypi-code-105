# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comptes', 'comptes.migrations']

package_data = \
{'': ['*'], 'comptes': ['templates/comptes/*']}

install_requires = \
['dmdm>=1.4.5,<2.0.0', 'ndh>=5.1.2,<6.0.0']

setup_kwargs = {
    'name': 'comptes',
    'version': '2.0.2',
    'description': 'Gestion des comptes',
    'long_description': None,
    'author': 'Guilhem Saurel',
    'author_email': 'guilhem.saurel@laas.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
