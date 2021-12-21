# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['azure_keyvault_browser',
 'azure_keyvault_browser.renderables',
 'azure_keyvault_browser.widgets']

package_data = \
{'': ['*']}

install_requires = \
['Whoosh>=2.7.4,<3.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'azure-identity>=1.7.1,<2.0.0',
 'azure-keyvault-secrets>=4.3.0,<5.0.0',
 'click>=8.0.3,<9.0.0',
 'pyperclip>=1.8.2,<2.0.0',
 'rich>=10.11.0,<11.0.0',
 'textual-inputs>=0.2.0,<0.3.0',
 'textual>=0.1.12,<0.2.0',
 'toml>=0.10.2,<0.11.0',
 'validators>=0.18.2,<0.19.0']

entry_points = \
{'console_scripts': ['kv = azure_keyvault_browser.app:run']}

setup_kwargs = {
    'name': 'azure-keyvault-browser',
    'version': '0.0.1',
    'description': 'A tool for browsing and searching for secrets in Azure Key Vault',
    'long_description': None,
    'author': 'Craig Gumbley',
    'author_email': 'craiggumbley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
