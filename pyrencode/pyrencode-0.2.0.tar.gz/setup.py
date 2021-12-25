# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyrencode', 'pyrencode.settings']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyrencode',
    'version': '0.2.0',
    'description': 'A pure python rencoder',
    'long_description': '=================================\npyrencode: rencode in pure python\n=================================\n\n.. image:: https://github.com/spapanik/pyrencode/actions/workflows/build.yml/badge.svg\n  :alt: Build\n  :target: https://github.com/spapanik/pyrencode/actions/workflows/build.yml\n.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/pyrencode.svg\n  :alt: Total alerts\n  :target: https://lgtm.com/projects/g/spapanik/pyrencode/alerts/\n.. image:: https://img.shields.io/github/license/spapanik/pyrencode\n  :alt: License\n  :target: https://github.com/spapanik/pyrencode/blob/main/LICENSE.txt\n.. image:: https://img.shields.io/pypi/v/pyrencode\n  :alt: PyPI\n  :target: https://pypi.org/project/pyrencode\n.. image:: https://pepy.tech/badge/pyrencode\n  :alt: Downloads\n  :target: https://pepy.tech/project/pyrencode\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n``pyrencode`` is a python rewrite of the original `rencode`_ by aresch, avoiding  the cython dependency, so that it can be used with PyPy.\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nThe easiest way is to use `poetry`_ to manage your dependencies and add *pyrencode* to them.\n\n.. code-block:: toml\n\n    [tool.poetry.dependencies]\n    pyrencode = "*"\n\nUsage\n^^^^^\n\n``pyrencode`` provides exactly the same interface as `rencode`_\n\n.. _rencode: https://github.com/aresch/rencode\n.. _poetry: https://python-poetry.org/\n\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _Changelog: https://github.com/spapanik/pyrencode/blob/main/CHANGELOG.rst\n.. _Documentation: https://pyrencode.readthedocs.io/en/latest/\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/pyrencode',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
