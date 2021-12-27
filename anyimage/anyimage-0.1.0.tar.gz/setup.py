# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anyim',
 'anyim.utils',
 'clip',
 'glide_text2im',
 'glide_text2im.clip',
 'glide_text2im.tokenizer',
 'tokenizer']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'attrs>=21.2.0,<22.0.0',
 'filelock>=3.4.2,<4.0.0',
 'fire>=0.4.0,<0.5.0',
 'ftfy>=6.0.3,<7.0.0',
 'regex>=2021.11.10,<2022.0.0',
 'requests>=2.26.0,<3.0.0',
 'torch>=1.10.1,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['anyim = anyim.main:main', 'anyimage = anyim.main:main']}

setup_kwargs = {
    'name': 'anyimage',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Richard Brooker',
    'author_email': 'richard@anghami.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
