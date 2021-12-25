# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['z4']
install_requires = \
['z3-solver>=4.8,<5.0']

setup_kwargs = {
    'name': 'z4-solver',
    'version': '2021.12.25.0',
    'description': 'z3++',
    'long_description': "z4\n============\n\n[z3](https://github.com/Z3Prover/z3) with some improvements:\n* Change the right shift operation on `BitVec`'s to be logical instead of arithmetic\n* Add the `ByteVec` class\n* Some helper methods for solving:\n  * `easy_solve`\n  * `find_all_solutions`\n  * `easy_prove`\n* Add some helper functions for z3 variables/constants:\n  * `BoolToInt`\n  * `Sgn`\n  * `Abs`\n  * `TruncDiv`\n",
    'author': 'Asger Hautop Drewsen',
    'author_email': 'asgerdrewsen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tyilo/z4',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
