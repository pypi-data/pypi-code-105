# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.gui', 'src.logic']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0',
 'logic>=0.2.3,<0.3.0',
 'ncbi-genome-download>=0.3.1,<0.4.0',
 'primer3-py>=0.6.1,<0.7.0',
 'requests>=2.26.0,<3.0.0',
 'wxPython>=4.1.1,<5.0.0']

entry_points = \
{'console_scripts': ['blast = src.blast:run_blast',
                     'mapping = src.mapping:mapping_genome',
                     'prepare = src.prepare:make_prepare',
                     'primer = src.primer_3:make_primers',
                     'splitter = src.splitter:make_split_sequence',
                     'start-gui = src.run_gui:run_my_app']}

setup_kwargs = {
    'name': 's3finder',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Polina Rasskazova',
    'author_email': 'rasskazova.pm@phystech.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
