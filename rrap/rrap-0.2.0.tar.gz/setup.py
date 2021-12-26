# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrap']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=0.16.0,<0.17.0',
 'matplotlib>=3.0.3,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'scipy>=1.5.2,<2.0.0',
 'sklearn>=0.0,<0.1',
 'threadpoolctl>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'rrap',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
