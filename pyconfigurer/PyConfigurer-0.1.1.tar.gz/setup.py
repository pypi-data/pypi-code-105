# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['PyConfigurer']

package_data = \
{'': ['*']}

install_requires = \
['PySimpleGUI>=4.55.1,<5.0.0', 'toml>=0.9,<0.10']

setup_kwargs = {
    'name': 'pyconfigurer',
    'version': '0.1.1',
    'description': 'A GUI configuration library for python programs.',
    'long_description': '# PyConfigurer\n\nA GUI configuration library for python programs.\n\n# Usage\n\n```python\nfrom PyConfigurer import Configurer, ConfigTemplate, Token, FieldType\n\n\ndefault_config = {\n    "user": "Arjix",\n    "age": 18\n}\n\n\nconfig_template = ConfigTemplate([\n    Token(FieldType.text_input, "user", "Enter your name:", default_config["user"]),\n    Token(FieldType.int_input, "age", "Enter your age:", default_config["age"])\n])\nconfig = Configurer(config_template)\nnew_config = config.run()\n\n\nprint("Old config", default_config)\nprint("New config", new_config)\n```\n',
    'author': 'ArjixWasTaken',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ArjixWasTaken/PyConfigurer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
