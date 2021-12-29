# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyba_client']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.4,<0.6.0',
 'marshmallow>=3.12.1,<4.0.0',
 'pandas>=1.3.2,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'tyba-client',
    'version': '0.1.18',
    'description': 'A Python API client for the Tyba Public API',
    'long_description': '# Tyba API Client\n\n### Run the examples in this codebase\n- Establish a SSH connection to the AWS bastion (enables access to the pricing DB)\n- Start the Generation docker image\n- Start the Tyba Server REPL\n- Finally, run the example script shown below in a virtual environment (provided by poetry):\n```\npoetry shell\npoetry install\nHOST=\'http://localhost:3000\' TYBA_PAT="dev-test-api-key"   python3 examples/pv_example.py\n```\n\n### Common Error Scenarios:\n#### Receiving a 401 Response\n- Check that the request is hitting the Tyba Server REPL\n- Check that the request is making it to the intended domain. (e.g., make sure the implementation of `Client` is reading the `HOST` env var)',
    'author': 'Tyler Nisonoff',
    'author_email': 'tyler@tybaenergy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
