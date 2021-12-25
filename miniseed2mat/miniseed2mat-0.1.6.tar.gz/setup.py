# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miniseed2mat']

package_data = \
{'': ['*']}

install_requires = \
['obspy>=1.2.2,<2.0.0', 'scipy>=1.7.3,<2.0.0']

entry_points = \
{'console_scripts': ['mseed2mat = miniseed2mat.main:convertmseed2mat']}

setup_kwargs = {
    'name': 'miniseed2mat',
    'version': '0.1.6',
    'description': 'Analyzing MiniSEED seismic data in MATLAB',
    'long_description': '## Analyzing MiniSEED seismic data in MATLAB \n\nFor details on the usage, visit the earthinversion post: https://www.earthinversion.com/utilities/converting-mseed-data-to-mat-and-analyzing-in-matlab/\n\n## Output data structure\n\n- `stats` contains all the meta data information corresponding to each trace, and\n- `data` contain the time series data\n\n```\nmat_file.mat -> stats, data\nstats -> stats_0, stats_1, ...\ndata -> data_0, data_1, ...\n```\n',
    'author': 'Utpal Kumar',
    'author_email': 'utpalkumar50@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.earthinversion.com/utilities/converting-mseed-data-to-mat-and-analyzing-in-matlab/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
