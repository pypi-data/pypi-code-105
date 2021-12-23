# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mathverse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mathverse',
    'version': '0.0.0.dev0',
    'description': 'Mathverse',
    'long_description': '# Mathverse\n',
    'author': 'The Vinh LUONG (LƯƠNG Thế Vinh)',
    'author_email': 'Edu.AI@STEAMforVietNam.org',
    'maintainer': 'The Vinh LUONG (LƯƠNG Thế Vinh)',
    'maintainer_email': 'Edu.AI@STEAMforVietNam.org',
    'url': 'https://GitHub.com/Mathverse/Mathverse',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
