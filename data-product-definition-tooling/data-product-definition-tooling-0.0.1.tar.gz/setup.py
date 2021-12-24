# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['converter', 'converter.tests', 'converter.tests.data.AirQuality']

package_data = \
{'': ['*'], 'converter.tests': ['__snapshots__/test_converter/*']}

install_requires = \
['deepdiff>=5.7.0,<6.0.0',
 'fastapi>=0.70.1,<0.71.0',
 'stringcase>=1.2.0,<2.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['converter = converter.cli:cli']}

setup_kwargs = {
    'name': 'data-product-definition-tooling',
    'version': '0.0.1',
    'description': 'Data Product Definition Tooling',
    'long_description': '# data-product-definition-tooling\n\nTools for managing Data Product definitions\n',
    'author': 'Digital Living International Ltd',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ioxio-nexus/data-product-definition-tooling',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0',
}


setup(**setup_kwargs)
