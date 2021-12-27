# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polybench', 'polybench.solvers']

package_data = \
{'': ['*'],
 'polybench.solvers': ['reform/*',
                       'reform/src/*',
                       'rings/*',
                       'rings/config/*',
                       'rings/gradle/wrapper/*',
                       'rings/src/main/java/com/github/tueda/polybench/rings/*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'colorlog>=6.6.0,<7.0.0',
 'importlib-metadata>=4.8.3,<5.0.0',
 'importlib-resources>=5.4.0,<6.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'pandas>=1.1.5,<2.0.0',
 'pretty-errors>=1.2.25,<2.0.0',
 'psutil>=5.8.0,<6.0.0',
 'py-cpuinfo>=8.0.0,<9.0.0',
 'symengine>=0.8.1,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'tomli>=1.2.3,<2.0.0',
 'typing-extensions>=4.0.1,<5.0.0']

extras_require = \
{':python_full_version >= "3.6.1" and python_full_version < "3.7.0"': ['kiwisolver==1.3.1',
                                                                       'numpy>=1.19.5,<1.20.0'],
 ':python_version >= "3.7" and python_version < "3.11"': ['kiwisolver>=1.3.2,<2.0.0',
                                                          'numpy>=1.21.5,<2.0.0']}

entry_points = \
{'console_scripts': ['polybench = polybench.__main__:entry_point']}

setup_kwargs = {
    'name': 'polybench',
    'version': '0.2.0rc1',
    'description': 'Multivariate polynomial arithmetic benchmark tests.',
    'long_description': 'polybench\n=========\n\n[![Test](https://github.com/tueda/polybench/workflows/Test/badge.svg?branch=master)](https://github.com/tueda/polybench/actions?query=branch:master)\n[![PyPI version](https://badge.fury.io/py/polybench.svg)](https://pypi.org/project/polybench/)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tueda/polybench.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tueda/polybench/context:python)\n\nMultivariate polynomial arithmetic benchmark tests.\n\nMany scientific and engineering applications utilise multivariate polynomial\narithmetic in their algorithms and solutions. Here we provide a set of\nbenchmark tests for often-used operations in multivariate polynomial\narithmetic:\n\n- Greatest common divisor\n- Factorisation\n\n\nRequirements\n------------\n\n- [Python](https://www.python.org/) >= 3.6.1\n\nYou also need at least one or more tools to be benchmarked.\nThey are (in alphabetical order):\n\n- [Fermat](https://home.bway.net/lewis/)\n- [FORM](https://www.nikhef.nl/~form/):\n  if not available in the system, then\n  a [release binary](https://github.com/vermaseren/form/releases)\n  will be automatically downloaded.\n- [Mathematica](https://www.wolfram.com/mathematica/):\n  indeed, [Free Wolfram Engine for Developers](https://www.wolfram.com/engine/) is sufficient to run.\n- [reFORM](https://reform.readthedocs.io/en/latest/):\n  automatically downloaded\n  (requires [Rust](https://www.rust-lang.org/) >= 1.36).\n- [Rings](https://ringsalgebra.io/):\n  automatically downloaded\n  (requires [JDK](https://www.oracle.com/technetwork/java/) >= 8).\n- [Singular](https://www.singular.uni-kl.de/)\n\n\nGetting started\n---------------\n\nClone this repository and try to run the `run.sh` script:\n\n```sh\ngit clone https://github.com/tueda/polybench.git\ncd polybench\n./run.sh --all\n```\n\nWhen starting the script for the first time, it automatically sets up\na virtual environment for required Python packages so that it will not dirty\nyour environment. Some of the tools are provided as libraries registered in\npublic package registries, so the first run takes some time to download,\ncompile and link them with test binaries. After testing, a CSV file and\ncomparison plots will be generated.\n\nFor practical benchmarking, configuration parameters should be set\nadequately. See the help message shown by\n\n```sh\n./run.sh --help\n```\n\nYou can also use [pip](https://pip.pypa.io/en/stable/),\n[pipx](https://pipxproject.github.io/pipx/),\n[Poetry](https://python-poetry.org/)\nor [Docker](https://www.docker.com/) with this repository.\nInstallation with `pip(x) install` or `poetry install` makes a command\n`polybench` available, which acts as the `run.sh` script described above.\n```sh\npip install polybench\npolybench --all\npython -m polybench --all  # alternative way to launch\n```\n```sh\npipx install polybench\npolybench --all\n```\n```sh\ngit clone https://github.com/tueda/polybench.git\ncd polybench\npoetry install\npoetry run polybench --all\n```\n```sh\ndocker build -t polybench:latest https://github.com/tueda/polybench.git\ndocker run -it --rm polybench:latest\n./run.sh --all\n```\n\n\nLicense\n-------\n\n[MIT](https://github.com/tueda/polybench/blob/master/LICENSE)\n',
    'author': 'Takahiro Ueda',
    'author_email': 'tueda@st.seikei.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tueda/polybench',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
