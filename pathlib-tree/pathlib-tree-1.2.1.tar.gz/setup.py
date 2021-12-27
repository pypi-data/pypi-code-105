# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pathlib_tree', 'pathlib_tree.mounts', 'pathlib_tree.mounts.platform']

package_data = \
{'': ['*']}

install_requires = \
['cli-toolkit>=1.2,<2.0', 'filemagic>=1.6,<2.0']

setup_kwargs = {
    'name': 'pathlib-tree',
    'version': '1.2.1',
    'description': 'Filesystem tree utilities',
    'long_description': None,
    'author': 'Ilkka Tuohela',
    'author_email': 'hile@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
