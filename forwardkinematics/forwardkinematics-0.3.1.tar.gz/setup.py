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
    'version': '0.3.1',
    'description': '"Light-weight implementation of forward kinematics using casadi."',
    'long_description': '# Installation\n\nThis package provides a forward kinematics for simple robots as symbolic functions using\ncasadi. This allows the usage in model predictive control schemes and other trajectory\noptimization methods.\n\n```bash\npip3 install -e .\n```\n',
    'author': 'Max Spahn',
    'author_email': 'm.spahn@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxspahn/forwardKinematics.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
