# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['Neutron']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.42.0,<4.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'keyboard>=0.13.5,<0.14.0',
 'lxml>=4.7.1,<5.0.0',
 'pycairo>=1.20.1,<2.0.0',
 'pywebview>=3.5,<4.0']

setup_kwargs = {
    'name': 'neutron-web',
    'version': '0.1.0',
    'description': "Neutron allows developers to build native Python apps along with CSS and HTML for frontend design. Based on pywebview for it's native GUI window and JavaScript-Python communicat.",
    'long_description': None,
    'author': 'IanTerzo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
