# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coco_utils']

package_data = \
{'': ['*']}

install_requires = \
['fastcore>=1.3.27,<2.0.0', 'pycocotools>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'coco-utils',
    'version': '0.0.1',
    'description': 'utility functions for data explorations and metrics calculation on coco data format',
    'long_description': None,
    'author': 'Prakash Jay',
    'author_email': 'prakashjyy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
