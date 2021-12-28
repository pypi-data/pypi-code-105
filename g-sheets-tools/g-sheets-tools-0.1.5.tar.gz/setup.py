# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['g-sheets-tools', 'g-sheets-tools.gsheetstools', 'g-sheets-tools.tests']

package_data = \
{'': ['*']}

install_requires = \
['cachetools==4.1.1',
 'certifi>=2021.10.8,<2022.0.0',
 'chardet>=4.0.0,<5.0.0',
 'google-api-client>=3.14.159265359,<4.0.0',
 'google-api-core>=2.3.2,<3.0.0',
 'google-api-python-client>=2.33.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.4.6,<0.5.0',
 'google-auth>=2.3.3,<3.0.0',
 'googleapis-common-protos>=1.54.0,<2.0.0',
 'httplib2>=0.20.2,<0.21.0',
 'idna>=3.3,<4.0',
 'numpy>=1.19.2,<2.0.0',
 'oauthlib>=3.1.1,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'protobuf>=3.19.1,<4.0.0',
 'pyasn1-modules>=0.2.8,<0.3.0',
 'pyasn1>=0.4.8,<0.5.0',
 'pytest>=6.2.5,<7.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2021.3,<2022.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'rsa>=4.8,<5.0',
 'six>=1.16.0,<2.0.0',
 'uritemplate>=4.1.1,<5.0.0',
 'urllib3>=1.26.7,<2.0.0']

setup_kwargs = {
    'name': 'g-sheets-tools',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Andy Friedman',
    'author_email': 'afriedman412@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
