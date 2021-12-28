# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyqt_feedback_flow']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0', 'emoji>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'pyqt-feedback-flow',
    'version': '0.1.0',
    'description': 'Show feedbacks in toast-like notifications',
    'long_description': None,
    'author': 'firefly-cpp',
    'author_email': 'iztok@iztok-jr-fister.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
