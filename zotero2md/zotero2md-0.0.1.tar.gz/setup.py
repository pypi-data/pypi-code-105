# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zotero2md', 'zotero2md.test']

package_data = \
{'': ['*']}

install_requires = \
['Pyzotero>=1.4.26,<2.0.0',
 'SnakeMD>=0.9.3,<0.10.0',
 'markdownify>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'zotero2md',
    'version': '0.0.1',
    'description': 'Export Zotero annotations and notes to Markdown files.',
    'long_description': '# Zotero to Markdown\n\nGenerate Markdown files from Zotero annotations (Zotero Beta). \nWith new Zotero PDF Reader and Note Editor, all highlights are saved in Zotero databases.\nThe highlights are NOT saved in the PDF file unless you export the highlights in order to save them.\n\n\n\n<a href="https://www.buymeacoffee.com/ealizadeh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>',
    'author': 'ealizadeh',
    'author_email': 'hello@ealizadeh.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/e-alizadeh/Zotero2MD',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
