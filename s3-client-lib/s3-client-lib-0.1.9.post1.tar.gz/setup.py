# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_client_lib']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.18,<2.0.0']

setup_kwargs = {
    'name': 's3-client-lib',
    'version': '0.1.9.post1',
    'description': 'S3 client lib',
    'long_description': '# S3 client lib\nLibrary for client calls to S3.\n\n## Installing\n\n* Install ```botos3``` system packages\n* Build & Install s3-client-lib with poetry:\n```python\npip install poetry\ngit clone https://github.com/CESNET/s3-client-lib\ncd s3-client-lib\npoetry build\ncd dist\ntar -xvf s3-client-lib-0.1.0.tar.gz\npip install -e s3-client-lib-0.1.0/\n```\n',
    'author': 'Radim Spigel',
    'author_email': 'spigel@cesnet.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
