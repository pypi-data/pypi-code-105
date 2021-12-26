# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_help']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'text-help',
    'version': '1.0.1',
    'description': "Text('Some text').translit(lang), .upper(), .lower(), .rus_to_eng(), eng_to_rus(); Cipher('Text for cipher').transposing(), .to_A1Z26(lang), from_A1Z26(lang); Support langs: Eng, Rus.",
    'long_description': None,
    'author': 'Dima',
    'author_email': 'ludina.work1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
