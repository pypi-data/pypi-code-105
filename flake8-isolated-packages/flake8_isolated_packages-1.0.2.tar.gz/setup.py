# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_isolated_packages']
install_requires = \
['astpretty>=2.1.0,<3.0.0', 'flake8>=4,<5']

entry_points = \
{'flake8.extension': ['FIP = flake8_isolated_packages:Plugin']}

setup_kwargs = {
    'name': 'flake8-isolated-packages',
    'version': '1.0.2',
    'description': 'This Flake8 plugin is for checking imports isolations.',
    'long_description': '# flake8_isolated_packages\n\nThis *Flake8* plugin is for checking imports isolations.  \n**One rule:** Any module from specified package could not be import in another package\n\n# Quick Start Guide\n\n1. Install ``flake8-isolated-packages`` from PyPI with pip::\n\n        pip install flake8-isolated-packages\n\n2. Configure a mark that you would like to validate::\n\n        cd project_root/\n        vi setup.cfg\n\n3. Add to file following: \n   \n        [flake8]  \n        isolated_packages = service, tests  \n        test_folders = tests\n\n3. Run flake8::\n\n        flake8 .\n\n# flake8 codes\n\n   * FIP100: You try to import from isolated package\n\n# Settings\n\n**isolated_packages**  \nIt specifies a list of folders, that cannot be imported outside of their package\n\n**test_folders**  \nIt specifies a list of folders, that contains tests and in which can be imported something from even isolated packages\n',
    'author': 'Dudov Dmitry',
    'author_email': 'dudov.dm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DDmitiy/flake8_isolated_packages',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
