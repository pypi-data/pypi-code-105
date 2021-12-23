# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_logo']

package_data = \
{'': ['*'], 'nonebot_plugin_logo': ['templates/*']}

install_requires = \
['Jinja2>=3.0.0,<4.0.0',
 'imageio>=2.12.0,<3.0.0',
 'nonebot-adapter-cqhttp>=2.0.0-alpha.15,<3.0.0',
 'nonebot-plugin-htmlrender>=0.0.1,<0.0.2',
 'nonebot2>=2.0.0-alpha.15,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-logo',
    'version': '0.1.0',
    'description': 'Nonebot2 plugin for making logo in PornHub or other styles',
    'long_description': None,
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
