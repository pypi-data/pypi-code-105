# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_code_meli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-code-meli',
    'version': '0.1.2',
    'description': 'This python package gives you a simple method that you can validate code meli (Iranian National Code) with it.',
    'long_description': 'This project is following this Unix philosophy:  [DOTADIW](https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well)\n\n\n____\n\nSo the project do a simple task.. validate code meli (Iranian National Code)..thats it..!\n\n\n\nthe algorithem is explained in Persian in [this site](http://www.aliarash.com/article/codemeli/codemeli.htm)',
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
