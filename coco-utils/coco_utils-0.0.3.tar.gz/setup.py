# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coco_utils']

package_data = \
{'': ['*']}

install_requires = \
['fastcore>=1.3.27,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pycocotools>=2.0.3,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'torch>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'coco-utils',
    'version': '0.0.3',
    'description': 'utility functions for data explorations and metrics calculation on coco data format',
    'long_description': '# coco_utils\nA set of utility functions to process object detection (coco) datasets.\n\n\n## Summary\n- **COCO wrapper**,  Use coco_utils COCO function which has extra properties like `label_counts`, `label_presence`, `img_wise_counts`, `label_names`, `label_names_available`, `count_images`. \n\n```python\nfrom coco_utils.coco import COCO\nx = COCO("data/annotations/instances_val2017.json")\n```\n\n- **`plot labels`** function is used to plot and save `labels_correlogram.jpg` and `labels.jpg` files. \n\n```python\nfrom coco_utils.plots import plot_coco_labels\nloc = "data/annotations/instances_val2017.json"\nplot_coco_labels(loc, "data/outputs/")\n```\n\n\n## Summary of set up\n\n- Clone the repo and do `poetry install`. To install poetry on your [system/server](https://github.com/prakashjayy/fullstack_dl/issues/17). \n\n> How to run tests ?\n- TODO \n\n> How to use ?\n- `poetry add coco_utils` or `pip install coco_utils`\n\n> Deployment instructions\n- `poetry build` & `poetry publish` \n\n\n## Who do I talk to?\n\n> Repo owner or admin\n- Prakash Vanapalli\n\n> Other community or team contact.\n',
    'author': 'Prakash Jay',
    'author_email': 'prakashjyy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/prakashjayy/coco_utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
