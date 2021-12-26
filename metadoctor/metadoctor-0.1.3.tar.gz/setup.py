# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metadoctor',
 'metadoctor..ipynb_checkpoints',
 'metadoctor.Trash',
 'metadoctor.Trash..ipynb_checkpoints',
 'metadoctor.Trash.models',
 'metadoctor.Trash.models..ipynb_checkpoints',
 'metadoctor.Trash.tuples',
 'metadoctor.Trash.tuples..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['MarkupSafe>=2.0.1,<3.0.0',
 'deta>=1.0.1,<2.0.0',
 'passlib[bcrypt]>=1.7.4,<2.0.0',
 'starlette>=0.17.1,<0.18.0']

setup_kwargs = {
    'name': 'metadoctor',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'arantesdv',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
