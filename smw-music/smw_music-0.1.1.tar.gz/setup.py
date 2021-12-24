# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smw_music', 'smw_music.scripts']

package_data = \
{'': ['*']}

install_requires = \
['music21>=7.1.0,<8.0.0']

entry_points = \
{'console_scripts': ['smw_music_xml_to_amk = smw_music.scripts.convert:main']}

setup_kwargs = {
    'name': 'smw-music',
    'version': '0.1.1',
    'description': 'Tools for working with SMW Music',
    'long_description': "SMW Music README\n================\n\n|bandit-status| |lint-status| |mypy-status| |test-status| |made-with-python|\n|made-with-sphinx-doc| |rtd-status| |reuse| |license|\n\nLibrary and utilities for generating AddMusicK-compatible MML files from\nMusicXML.\n\nThe tooling has only been tested with exported MusicXML files from MuseScore\n3.6.2, but it should work with outputs from other music notation software.\n\nThe software (and especially the libraries) are pre-alpha.  APIs may change at\nany time for any/no reason.\n\nInstallation\n------------\n\nUse `pip <https://pip.pypa.io/en/stable>`_ to install ``smw_music``:\n\n.. code-block:: bash\n\n   pip install smw_music\n\nOr install from source using `poetry <https://python-poetry.org/>`_:\n\n.. code-block:: bash\n\n   pip install poetry\n   git clone https://github.com/com-posers-pit/\n   poetry install --no-dev\n\nUsage\n-----\n\nAfter installing the tools, convert a MusicXML file ``song.mxl`` to an\nAddMusicK MML file ``song.txt`` by running the following command:\n\n.. code-block:: bash\n\n   smw_music_xml_to_amk  song.xml song.txt\n\nSee `Examples`_ in the official documentation for more detailed examples.\n\nContributing\n------------\n\nPull requests are welcome.  See our `Contributor Guide`_ for information.\n\nLicense\n-------\n\nThe SMW Music Python Project\nCopyright (C) 2021  `The SMW Music Python Project Authors`_\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU Affero General Public License as\npublished by the Free Software Foundation, either version 3 of the\nLicense, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU Affero General Public License for more details.\n\nYou should have received a copy of the GNU Affero General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>.\n\nA copy of the AGPL v3.0 is available `here <License_>`_\n\nAcknowledgements\n----------------\n\n- Kipernal, KungFuFurby, and other authors of `AddMusicK`_\n- Wakana's `SMW music porting tutorial`_\n- Michael Scott Cuthbert and cuthbertLab's `music21 Python library`_\n\n.. # Links\n.. _Examples: https://smw-music.readthedocs.io/en/latest/examples.html\n.. _The SMW Music Python Project Authors: https://github.com/com-posers-pit/smw_music/blob/develop/AUTHORS.rst\n.. _License: https://github.com/com-posers-pit/smw_music/blob/develop/LICENSES/AGPL-3.0-only.txt\n.. _Contributor Guide:  https://github.com/com-posers-pit/smw_music/blob/develop/CONTRIBUTING.rst\n.. _AddMusicK: https://www.smwcentral.net/?p=section&a=details&id=24994\n.. _SMW music porting tutorial: https://www.smwcentral.net/?p=viewthread&t=89606\n.. _music21 Python library: https://github.com/cuthbertLab/music21\n.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg\n   :target: https://www.python.org/\n.. |made-with-sphinx-doc| image:: https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg\n   :target: https://www.sphinx-doc.org/\n.. |rtd-status| image:: https://readthedocs.org/projects/smw-music/badge/?version=latest\n   :target: https://smw-music.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n.. |bandit-status| image:: https://github.com/com-posers-pit/smw_music/actions/workflows/bandit.yml/badge.svg\n   :target: https://github.com/\n.. |lint-status| image:: https://github.com/com-posers-pit/smw_music/actions/workflows/lint.yml/badge.svg\n   :target: https://github.com/\n.. |mypy-status| image:: https://github.com/com-posers-pit/smw_music/actions/workflows/mypy.yml/badge.svg\n   :target: https://github.com/\n.. |test-status| image:: https://github.com/com-posers-pit/smw_music/actions/workflows/test.yml/badge.svg\n   :target: https://github.com/\n.. |license| image:: https://img.shields.io/badge/License-AGPLv3-blue.svg\n.. |reuse| image:: https://api.reuse.software/badge/github.com/com-posers-pit/smw_music\n   :target: https://api.reuse.software/info/github.com/com-posers-pit/smw_music\n",
    'author': 'Thomas A. Werne',
    'author_email': 'werneta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/com-posers-pit/smw_music',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
