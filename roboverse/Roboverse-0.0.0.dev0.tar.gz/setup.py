# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['roboverse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'roboverse',
    'version': '0.0.0.dev0',
    'description': 'Robotics Metaverse',
    'long_description': '# `Roboverse`: Robotics Metaverse\n',
    'author': 'The Vinh LUONG (LƯƠNG Thế Vinh)',
    'author_email': 'Vinh@STEAMforVietNam.org',
    'maintainer': 'The Vinh LUONG (LƯƠNG Thế Vinh)',
    'maintainer_email': 'Vinh@STEAMforVietNam.org',
    'url': 'https://GitHub.com/Mindstem/Roboverse',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
