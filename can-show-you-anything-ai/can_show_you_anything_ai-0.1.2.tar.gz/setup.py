# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clip',
 'glide_text2im',
 'glide_text2im.clip',
 'glide_text2im.tokenizer',
 'show_anything',
 'show_anything.utils',
 'tokenizer']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'attrs>=21.2.0,<22.0.0',
 'filelock>=3.4.2,<4.0.0',
 'fire>=0.4.0,<0.5.0',
 'folium==0.2.1',
 'ftfy>=6.0.3,<7.0.0',
 'imgaug==0.2.6',
 'regex>=2021.11.10,<2022.0.0',
 'requests==2.23.0',
 'torch>=1.10.0,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['show_me_a = show_anything:cli',
                     'showme = show_anything:cli',
                     'showmea = show_anything:cli']}

setup_kwargs = {
    'name': 'can-show-you-anything-ai',
    'version': '0.1.2',
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
