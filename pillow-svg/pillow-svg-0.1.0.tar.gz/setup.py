# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pillow_svg']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0']

setup_kwargs = {
    'name': 'pillow-svg',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'djkcyl',
    'author_email': 'cyl@cyllive.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gribbg/pillow_svg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
