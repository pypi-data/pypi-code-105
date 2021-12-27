# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uboxadmin',
 'uboxadmin.cool',
 'uboxadmin.jwt',
 'uboxadmin.management',
 'uboxadmin.management.commands',
 'uboxadmin.migrations',
 'uboxadmin.models',
 'uboxadmin.views',
 'uboxadmin.views.base',
 'uboxadmin.views.base.plugin',
 'uboxadmin.views.base.sys',
 'uboxadmin.views.space']

package_data = \
{'': ['*']}

install_requires = \
['Django>=1.11.8,<2.0.0',
 'captcha>=0.3,<0.4',
 'djangorestframework-camel-case>=1.2.0,<2.0.0',
 'djangorestframework-simplejwt==4.3.0',
 'djangorestframework==3.11.2',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'uboxadmin',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'heweitao',
    'author_email': '675428202@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
