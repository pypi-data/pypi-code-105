# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['validate_cnpj']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'validate-cnpj',
    'version': '0.0.1',
    'description': 'Faz a validação de CNPJ Brasileiro',
    'long_description': "# validate-cnpj\n\n[![pipy](https://img.shields.io/pypi/v/validate_cnpj.svg)](https://pypi.python.org/pypi/validate_cnpj)\n\nValidates Brazilian CNPJ\n\n## Features\n\n- CNPJ Validation with mask\n- CNPJ Validation without mask\n\n## Modes of use\n\n```python\n#!/usr/bin/python\nimport validate_cnpj\n\n# Without mask\nvalidate_cnpj.is_valid('40158686000170') # True\n\n# With mask\nvalidate_cnpj.is_valid('40.158.686/0001-70') # True\n```\n\nor\n\n```python\n#!/usr/bin/python\nfrom validate_cnpj import is_valid\n\n# Without mask\nis_valid('11.111.111/0001-11') # False\n\n# With mask\nis_valid('11111111000111') # False\n```\n\n# Author\n\n[João Filho](https://joaofilho.dev)\n[Github](https://github.com/drummerzzz)\n\n# Credits\n\nThis package was created with Cookiecutter and the `cs01/cookiecutter-pypackage` project template.\n\n[Cookiecutter](https://github.com/audreyr/cookiecutter)\n\n[cs01/cookiecutter-pypackage](https://github.com/cs01/cookiecutter-pypackage)\n",
    'author': 'Drummerzzz',
    'author_email': 'devdrummerzzz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drummerzzz/pypi_validate_cnpj/README.md',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
