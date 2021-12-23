# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forwardkinematics',
 'forwardkinematics.fksCommon',
 'forwardkinematics.planarFks',
 'forwardkinematics.urdfFks',
 'forwardkinematics.urdfFks.casadiConversion',
 'forwardkinematics.urdfFks.casadiConversion.geometry']

package_data = \
{'': ['*'], 'forwardkinematics.urdfFks': ['urdf/*']}

install_requires = \
['casadi==3.5.1', 'numpy>=1.15.5,<2.0.0', 'urdf_parser_py==0.0.3']

setup_kwargs = {
    'name': 'forwardkinematics',
    'version': '0.3.0',
    'description': '"Light-weight implementation of forward kinematics using casadi."',
    'long_description': None,
    'author': 'Max Spahn',
    'author_email': 'm.spahn@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
