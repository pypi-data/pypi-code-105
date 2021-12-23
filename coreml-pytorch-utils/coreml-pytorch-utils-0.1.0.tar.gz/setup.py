
# -*- coding: utf-8 -*-
from setuptools import setup

long_description = None
INSTALL_REQUIRES = [
    'coremltools>=5.0',
    'future',
]

setup_kwargs = {
    'name': 'coreml_pytorch_utils',
    'version': '0.1.0',
    'description': 'Coreml utils that helps export pytorch based models',
    'long_description': long_description,
    'license': 'EUPL-1.2',
    'author': '',
    'author_email': 'machineko <machineko@protonmail.com>',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/machineko/coreml_torch_utils',
    'packages': [
        'coreml_utils.tests',
        'coreml_utils.utils',
    ],
    'package_data': {'': ['*']},
    'install_requires': INSTALL_REQUIRES,
    'python_requires': '>=3.9',

}


setup(**setup_kwargs)
