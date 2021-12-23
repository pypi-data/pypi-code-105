# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pumpkin_py',
 'pumpkin_py.builder',
 'pumpkin_py.config',
 'pumpkin_py.graph',
 'pumpkin_py.models',
 'pumpkin_py.sim',
 'pumpkin_py.store',
 'pumpkin_py.utils']

package_data = \
{'': ['*']}

install_requires = \
['bidict>=0.21.2,<0.22.0',
 'numpy>=1.19.0,<2.0.0',
 'pyroaring>=0.3.2,<0.4.0',
 'rdflib>=5.0.0,<6.0.0']

setup_kwargs = {
    'name': 'pumpkin-py',
    'version': '0.0.2',
    'description': 'Fast semantic search and comparison',
    'long_description': 'PumpkinPy - Semantic similarity implemented in python\n\n##### About\n\nPumpkinPy uses IC ordered bitmaps for fast ranking of genes and diseases\n(phenotypes are sorted by descending frequency and one-hot encoded).\nThis is useful for larger ontologies such as Upheno and large datasets such\nas ranking all mouse genes given a set of input HPO terms.\nThis approach was first used in OWLTools and OwlSim-v3.\n\nThe goal of this project was to build an implementation of the PhenoDigm algorithm in python.\nThere are also implementations for common measures for distance and similarity\n(euclidean, cosine, Jin-Conrath, Resnik, jaccard)\n\n*Disclaimer*: This is a side project needs more documentation and testing\n\n#### Getting Started\n\nRequires python 3.8+ and python3-dev to install pyroaring\n\n##### Installing from pypi\n\n```\npip install pumpkin_py\n```\n\n##### Building locally\nTo build locally first install poetry - \n\nhttps://python-poetry.org/docs/#installation\n\nThen run make:\n\n```make```\n\n##### Usage\n\nGet a list of implemented similarity measures\n```python\nfrom pumpkin_py import get_methods\nget_methods()\n[\'jaccard\', \'cosine\', \'phenodigm\', \'symmetric_phenodigm\', \'resnik\', \'symmetric_resnik\', \'ic_cosine\', \'sim_gic\']\n```\n\nLoad closures and annotations\n\n```python\nimport gzip\nfrom pathlib import Path\n\nfrom pumpkin_py import build_ic_graph_from_closures, flat_to_annotations, search\n\nclosures = Path(\'.\') / \'data\' / \'hpo\' / \'hp-closures.tsv.gz\'\nannotations = Path(\'.\') / \'data\' / \'hpo\' / \'phenotype-annotations.tsv.gz\'\n\nroot = "HP:0000118"\n\nwith gzip.open(annotations, \'rt\') as annot_file:\n    annot_map = flat_to_annotations(annot_file)\n\nwith gzip.open(closures, \'rt\') as closure_file:\n    graph = build_ic_graph_from_closures(closure_file, root, annot_map)\n```\n\nSearch for the best matching disease given a phenotype profile\n\n```python\nimport pprint\nfrom pumpkin_py import search\n\nprofile_a = (\n    "HP:0000403,HP:0000518,HP:0000565,HP:0000767,"\n    "HP:0000872,HP:0001257,HP:0001263,HP:0001290,"\n    "HP:0001629,HP:0002019,HP:0002072".split(\',\')\n)\n\nsearch_results = search(profile_a, annot_map, graph, \'phenodigm\')\n\npprint.pprint(search_results.results[0:5])\n```\n```\n[SimMatch(id=\'ORPHA:94125\', rank=1, score=72.67599348696685),\n SimMatch(id=\'ORPHA:79137\', rank=2, score=71.57368233248252),\n SimMatch(id=\'OMIM:619352\', rank=3, score=70.98305459477629),\n SimMatch(id=\'OMIM:618624\', rank=4, score=70.94596234638497),\n SimMatch(id=\'OMIM:617106\', rank=5, score=70.83097366257857)]\n```\n\n\n##### Example scripts for fetching Monarch annotations and closures\n\nUses robot and sparql to generate closures and class labels\n\nAnnotation data is fetched from the latest Monarch release\n - Requires >Java 8\n \n```cd data/monarch/ && make```\n\n\nPhenoDigm Reference: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3649640/  \nExomiser: https://github.com/exomiser/Exomiser  \nOWLTools: https://github.com/owlcollab/owltools  \nOWLSim-v3: https://github.com/monarch-initiative/owlsim-v3  \n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.9',
}


setup(**setup_kwargs)
