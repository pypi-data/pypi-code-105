# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['python_brtools']

package_data = \
{'': ['*']}

install_requires = \
['validate-cnpj>=0.0.1,<0.0.2', 'validate-cpf>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'python-brtools',
    'version': '0.0.1',
    'description': 'Validate CPF and CNPJ',
    'long_description': "# BRtools\n\n[![pipy](https://img.shields.io/pypi/v/brtools.svg)](https://pypi.python.org/pypi/brtools)\n\nBrazilian Validators\n\n## Features\n\n- CPF Validation with or without mask\n- CNPJ Validation with or without mask\n\n## Modes of use\n\n- CPF\n\n```python\n#!/usr/bin/python\nfrom brtools import validators\n\n# Without mask\nvalidators.is_valid_cnpj('40158686000170') # True\n\n# With mask\nvalidators.is_valid_cnpj('40.158.686/0001-70') # True\n```\n\n- CNPJ\n\n```python\n#!/usr/bin/python\nfrom brtools import validators\n\n# Without mask\nvalidators.is_valid_cnpj('40158686000170') # True\n\n# With mask\nvalidators.is_valid_cnpj('40.158.686/0001-70') # True\n```\n\n# Author\n\n[João Filho](https://joaofilho.dev)\n[Github](https://github.com/drummerzzz)\n\n# Credits\n\nThis package was created with Cookiecutter and the `cs01/cookiecutter-pypackage` project template.\n\n[Cookiecutter](https://github.com/audreyr/cookiecutter)\n\n[cs01/cookiecutter-pypackage](https://github.com/cs01/cookiecutter-pypackage)\n",
    'author': 'Drummerzzz',
    'author_email': 'devdrummerzzz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drummerzzz/pypi_brtools/README.md',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
