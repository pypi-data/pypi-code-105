# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['usgs', 'usgs.tests', 'usgs.tests.stubs']

package_data = \
{'': ['*']}

install_requires = \
['clint>=0.5.1,<0.6.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.26.0,<3.0.0',
 'urllib3==1.26.7']

setup_kwargs = {
    'name': 'usgs-m2m-api',
    'version': '0.2.0',
    'description': 'An object oriented method for working with the USGS EE machine-2-machine API v1.5',
    'long_description': '# USGS Python API\n\nAn object oriented wrapper around the USGS Earth Explorer JSON API (v1.5.x). The primary objective of this API is to provide a convenient method of requesting and downloading scenes from EE datasets, including robust metadata where available.\n\n## API Documentation\nhttps://cast.git-pages.uark.edu/transmap-hub/usgs/usgs/\n\n## Prerequisites\n- Must have an Earth Explorer account: https://earthexplorer.usgs.gov\n- The EE account must have M2M accesss, requested here: https://ers.cr.usgs.gov/profile/access (you will need to wait for approval)\n\n## Installation and Setup\n\n### Three methods for using your username and password\n1. Using a `.env` file\n```\nEE_USER="user_name"\nEE_PASS="user_pass"\n```\n2. Set your environment variables manually\n```bash\n$ export EE_USER="user_name"\n$ export EE_PASS="user_pass"\n```\n3. During each execution you will be prompted for your user:pass if one of the above two options are not set\n4. Hard code within script (not recommended) - see below\n\n### Installation (development)\n\n```python\n$ pipenv install\n$ pipenv run python ./example.py\n```\n\n### Basic API structure\nTo query a specific item, like a `dataset` or a `scene`, you need to construct a `Query` object from that namespace (`dataset.Query`, `scene.Query`) and pass that to the `Api` with either a `fetch` or `fetchone`. This will return a `Model` or `List[Model]` of that type (`dataset.Model`, `scene.Model`)\n\n\n_Initialize the API_\n```python\nfrom usgs_api import Api\napi = Api.login()\n### If you want to directly type your user:password you can use\napi = Api(username="user_name", password="password")\n```\n_Query a dataset by name_\n```python\ndataset = api.dataset(datasetName="corona2")\n```\n_Start a scene cursor with a list of scenes_\n```python\nscene_cursor = dataset.scenes()\n```\n_Collect only available scenes to queue for download_\n```python\ndownloadable = scene_cursor.downloadable\n```\n_Iterate the cursor to collect more scenes_\n```python\ndownloadable += scene_cursor.next().downloadable\n```\n_Enqueue the scenes for download from the Api_\n```python\napi.download(scenes)\n```\n_Start the download and automate the extraction_\n```python\napi.start_download(extract=True)\n```\n\n\n\n\n',
    'author': 'Christopher Angel',
    'author_email': 'cangel@uark.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
