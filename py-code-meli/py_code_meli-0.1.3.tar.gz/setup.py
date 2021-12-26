# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_code_meli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-code-meli',
    'version': '0.1.3',
    'description': 'This python package gives you a simple method that you can validate code meli (Iranian National Code) with it.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/py-code-meli.svg)](https://badge.fury.io/py/py-code-meli)\n\n\nThis project is following this Unix philosophy:  [DOTADIW](https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well)\n\n\n____\n\nSo the project do a simple task.. validate code meli (Iranian National Code)..thats it..!\n\n\n\nthe algorithem is explained in Persian in [this site](http://www.aliarash.com/article/codemeli/codemeli.htm)\n\n___\n## How to use it?\n\nto install it, run:\n>`pip install py-code-meli`\n\n```python\n>>>from py_code_meli import is_valid\n>>>is_valid("0095017240")\nTrue\n>>>is_valid("0095017241")\nFalse\n```\n\n\n___\n### Run Tests\n\nto run the package tests, first you need to clone it and then  run :\n\n>`poetry install`\n\nto run the tests:\n>`poetry run pytest`\n\n\n____\n**to generate valid code meli, use this [link](http://mellicode.azmads.com/Home/Index?id=0)**',
    'author': 'ali',
    'author_email': 'lmntrix.afr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rabbitix/py_code_meli',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
