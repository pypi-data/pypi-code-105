# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['napari_tiler', 'napari_tiler._tests']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata<4.3',
 'napari-plugin-engine>=0.2.0,<0.3.0',
 'numpy>=1.21.4,<2.0.0',
 'tiler>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'napari-tiler',
    'version': '0.0.4',
    'description': 'N-dimensional tiling and merging support for napari',
    'long_description': '# napari-tiler\n\n[![License](https://img.shields.io/pypi/l/napari-tiler.svg?color=green)](https://github.com/tdmorello/napari-tiler/raw/main/LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/napari-tiler.svg?color=green)](https://pypi.org/project/napari-tiler)\n[![Python Version](https://img.shields.io/pypi/pyversions/napari-tiler.svg?color=green)](https://python.org)\n[![tests](https://github.com/tdmorello/napari-tiler/workflows/tests/badge.svg)](https://github.com/tdmorello/napari-tiler/actions)\n[![codecov](https://codecov.io/gh/tdmorello/napari-tiler/branch/main/graph/badge.svg)](https://codecov.io/gh/tdmorello/napari-tiler)\n[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-tiler)](https://napari-hub.org/plugins/napari-tiler)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/napari-tiler.svg)](https://pypistats.org/packages/napari-tiler)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n[![Development Status](https://img.shields.io/pypi/status/napari-tiler.svg)](https://github.com/peng-lab/napari-tiler)\n\nN-dimensional tiling and merging support for napari\n\nThis plugin allows the user to split an image into a stack of tiles and subsequently merge the tiles to reconstruct the orignal image.\nSee [Tiler](https://github.com/the-lay/tiler) for more details.\n\n----------------------------------\n\nThis [napari] plugin was generated with [Cookiecutter] using [@napari]\'s [cookiecutter-napari-plugin] template.\n\n<!--\nDon\'t miss the full getting started guide to set up your new package:\nhttps://github.com/napari/cookiecutter-napari-plugin#getting-started\n\nand review the napari docs for plugin developers:\nhttps://napari.org/plugins/stable/index.html\n-->\n\n## Installation\n\n### Option 1 (recommended)\n\nYou can install `napari-tiler` from the napari plugin manager. Go to `Plugins -> Install/Uninstall Package(s)`, then search for `napari-tiler`. Click `Install`.\n\n### Option 2\n\nYou can also install `napari-tiler` via [pip]:\n\n    pip install napari-tiler\n\nTo install latest development version:\n\n    pip install git+https://github.com/tdmorello/napari-tiler.git\n\n## Quick Start\n\n1. Open a file in napari. The file may have any number of dimensions (e.g. z-stack, time series, ...)\n2. Start the plugin ( `Plugins -> napari-tiler: make_tiles` )\n3. Select the input layer from the dropdown box\n4. Select parameters for tiling\n5. Click `Run`\n\n## Contributing\n\nThis project uses [Poetry](https://github.com/python-poetry/poetry) for dependency management.\nTo set up the development environment, it is recommended to use:\n\n    conda env create -f environment.yaml\n\nContributions are very welcome. Tests can be run with [tox], please ensure the coverage at least stays the same before you submit a pull request.\n\n## License\n\nDistributed under the terms of the [BSD-3] license,\n"napari-tiler" is free and open source software\n\n## Issues\n\nIf you encounter any problems, please [file an issue] along with a detailed description.\n\n[napari]: https://github.com/napari/napari\n[Cookiecutter]: https://github.com/audreyr/cookiecutter\n[@napari]: https://github.com/napari\n[MIT]: http://opensource.org/licenses/MIT\n[BSD-3]: http://opensource.org/licenses/BSD-3-Clause\n[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt\n[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt\n[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0\n[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt\n[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin\n\n[file an issue]: https://github.com/tdmorello/napari-tiler/issues\n\n[napari]: https://github.com/napari/napari\n[tox]: https://tox.readthedocs.io/en/latest/\n[pip]: https://pypi.org/project/pip/\n[PyPI]: https://pypi.org/\n',
    'author': 'Tim Morello',
    'author_email': 'tdmorello@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
