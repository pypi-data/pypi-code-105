# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['catbird',
 'catbird.apis',
 'catbird.core',
 'catbird.core.utils',
 'catbird.core.utils.fileio',
 'catbird.core.utils.fileio.handlers',
 'catbird.datasets',
 'catbird.models',
 'catbird.models.losses']

package_data = \
{'': ['*']}

install_requires = \
['addict>=2.4.0,<3.0.0',
 'datasets>=1.16.1,<2.0.0',
 'pytorch-ignite>=0.4.7,<0.5.0',
 'sentencepiece>=0.1.96,<0.2.0',
 'tensorboardX>=2.4.1,<3.0.0',
 'torch>=1.10.0,<2.0.0',
 'transformers>=4.14.1,<5.0.0']

setup_kwargs = {
    'name': 'catbird',
    'version': '0.0.2',
    'description': 'Paraphrase generation Toolbox and Benchmark',
    'long_description': '<div align="center">\n    </p>\n    <img src="resources/catbird_logo.svg" width="200"/>\n    </p>\n\n  [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)\n</div>\n\n`Catbird` is an open source paraphrase generation toolkit based on PyTorch.\n\n## Quick Start\n\n### Requirements and Installation\nThe project is based on PyTorch 1.5+ and Python 3.6+.\n\n## Install Catbird\n\n**a. Clone the repository.**\n```shell\ngit clone https://github.com/AfonsoSalgadoSousa/catbird.git\n```\n**b. Install dependencies.**\nThis project uses Poetry as its package manager. There should Make sure you have it installed. For more info check [Poetry\'s official documentation](https://python-poetry.org/docs/).\nTo install dependencies, simply run:\n```shell\npoetry install\n```\n\n## Dataset Preparation\nFor now, we only work with the [Quora Question Pairs dataset](https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs). It is recommended to download and extract the datasets somewhere outside the project directory and symlink the dataset root to `$CATBIRD/data` as below. If your folder structure is different, you may need to change the corresponding paths in config files.\n\n```text\ncatbird\n├── catbird\n├── tools\n├── configs\n├── data\n│   ├── quora\n│   │   ├── quora_duplicate_questions.tsv\n```\nWe use the [HuggingFace Datasets library](https://huggingface.co/docs/datasets/) to load the datasets.\n\n### Train\n\n```shell\npoetry run python tools/train.py ${CONFIG_FILE} [optional arguments]\n```\n\nExample:\n1. Train T5 on QQP.\n```bash\n$ python tools/train.py configs/t5_quora.yaml\n```\n\n## Contributors\n* [Afonso Sousa][1] (afonsousa2806@gmail.com)\n\n[1]: https://github.com/AfonsoSalgadoSousa',
    'author': 'Afonso Sousa',
    'author_email': 'afonsousa2806@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AfonsoSalgadoSousa/catbird',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
