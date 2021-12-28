# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_htmlrender']

package_data = \
{'': ['*'], 'nonebot_plugin_htmlrender': ['templates/*']}

install_requires = \
['jinja2>=3.0.3,<4.0.0',
 'markdown>=3.3.6,<4.0.0',
 'nonebot-adapter-cqhttp>=2.0.0-alpha.16,<3.0.0',
 'nonebot2>=2.0.0-alpha.16,<3.0.0',
 'playwright>=1.17.2,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-htmlrender',
    'version': '0.0.2',
    'description': '',
    'long_description': '# nonebot-plugin-htmlrender\n\n* 通过浏览器渲染图片\n* 可通过查看`example`参考使用实例\n* ~~文档还没写~~',
    'author': 'kexue',
    'author_email': 'xana278@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
