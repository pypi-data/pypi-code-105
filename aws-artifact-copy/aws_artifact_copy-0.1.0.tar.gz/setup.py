# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_artifact_copy', 'aws_artifact_copy.common', 'aws_artifact_copy.services']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore>=2.1.0,<3.0.0',
 'trio-asyncio>=0.12.0,<0.13.0',
 'trio>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['aws-artifact-copy = aws_artifact_copy.cli:main']}

setup_kwargs = {
    'name': 'aws-artifact-copy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chaz Schlarp',
    'author_email': 'schlarpc@gmail.com',
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
