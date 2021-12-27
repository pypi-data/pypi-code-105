# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigearthnet_common']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'fastcore>=1.3,<2.0',
 'geopandas>=0.10,<0.11',
 'natsort>=8,<9',
 'pyarrow>=6,<7',
 'pydantic>=1.8,<2.0',
 'pygeos>=0.12,<0.13',
 'rich>=10,<11',
 'typer>=0.4,<0.5']

entry_points = \
{'console_scripts': ['ben_gdf_builder = '
                     'bigearthnet_common.gdf_builder:_run_gdf_cli']}

setup_kwargs = {
    'name': 'bigearthnet-common',
    'version': '0.1.1',
    'description': 'A collection of common tools to interact with the BigEarthNet dataset.',
    'long_description': "# Common BigEarthNet Tools\n> A personal collection of common tools to interact with the BigEarthNet dataset.\n\n\nThis library provides a collection of high-level tools to better work with the [BigEarthNet](bigearth.net) dataset.\n\n`ben_common` tries to accomplish three goals:\n\n1. Collect the most relevant _constants_ into a single place to reduce the time spent looking for these, like:\n   - The 19 or 43 class nomenclature strings\n   - URL\n   - Band statistics (mean/variance) as integer and float\n   - Channel names\n   - etc.\n2. Provide parsing functions to convert the metadata json files to a [geopandas](https://geopandas.org/en/stable/) [GeoDataFrame's](https://geopandas.org/en/stable/getting_started/introduction.html).\n   - Allow for easy top-level statistical analysis of the data in a familiar _pandas_-style \n   - Provide functions to enrich GeoDataFrames with often required BigEarthNet metadata (like the season or country of the patch)\n3. Simplify the building procedure by providing a command-line interface with reproducible results\n\n\n\n## Deep Learning \n\nOne of the main purposes of the dataset is to allow deep learning researchers and practitioners to train their model on multi-spectral satellite data easily.\nIn that regard, there is a general recommendation to drop patches that are covered by seasonal snow or clouds.\nAlso, the novel 19-class nomenclature should be preferred over the original 43-class nomenclature.\nAs a result of these recommendations, some patches have to be _excluded_ from the original raw BigEarthNet dataset that is provided at [BigEarthNet](bigearth.net).\nThis is especially important for higher-level statistical analysis.\n\nTo simplify the procedure of pre-converting the json metadata files, the library provides a single command that will generate a recommended GeoDataFrame with extra metadata (country/season data of each patch) while dropping all patches that are not recommended for deep learning research.\n\nTo generate such a GeoDataFrame and store it as an `parquet` file, use:\n\n- `gdf_builder build-recommended-parquet` (available after installing package) or\n- `python -m bigearthnet_common.gdf_builder build-recommended-parquet`\n\nIf you want to read the raw json files and convert those to a GeoDataFrame file, without dropping any patches or adding any metadata, use:\n\n- `gdf_builder build-raw-ben-parquet` (available after installing package) or\n- `python -m bigearthnet_common.gdf_builder build-raw-ben-parquet`\n\n\n## Local Installation\n\nUse [just](https://github.com/casey/just#installation) to install the package or run steps from `justfile` directly.\nRequires [mamba](https://github.com/mamba-org/mamba) (highly recommended) or [poetry](https://python-poetry.org/docs/basic-usage/) to be installed.\n\n## Local Documentation\n{% include note.html content='Building and serving the documentation requires `Docker` to be installed!' %}\nAfter creating the `ben_common_env` environment, run \n```bash\ndocker-compose up\n```\n\nOr with `just`:\n```bash\njust docs\n```\n\nAfter running the command, the documentation server will be available at \n- <http://0.0.0.0:4000/bigearthnet_common/> or \n- <http://localhost:4000/bigearthnet_common/> (WSL).\n\nTo review the source code, please look at the corresponding `ipynb` notebook from the `nbs` folder.\nThese notebooks include extensive documentation, visualizations, and tests.\nThe automatically generated Python files are available in the `bigearthnet_common` module.\n\n",
    'author': 'Kai Norman Clasen',
    'author_email': 'snakemap_navigation@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai-tub/bigearthnet_common',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
