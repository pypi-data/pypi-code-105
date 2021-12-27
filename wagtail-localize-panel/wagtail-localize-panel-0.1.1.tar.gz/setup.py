# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wagtail_localize_panel', 'wagtail_localize_panel.migrations']

package_data = \
{'': ['*'],
 'wagtail_localize_panel': ['templates/wagtail_localize_panel/home/*']}

install_requires = \
['Django>=3.2.4,<4.0.0', 'wagtail-localize>=1.0,<2.0', 'wagtail>=2.14.1,<3.0.0']

setup_kwargs = {
    'name': 'wagtail-localize-panel',
    'version': '0.1.1',
    'description': 'Wagtail localize panel and notification',
    'long_description': None,
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gandi.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
