# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['log4j_detector_to_csv']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['log4j-detector-to-csv = log4j_detector_to_csv.main:main']}

setup_kwargs = {
    'name': 'log4j-detector-to-csv',
    'version': '0.1.7',
    'description': 'Combines all host specific json outputs from log4j-detector into one single csv file.',
    'long_description': '# log4j-detector-to-csv\n\nThis project contains a script to convert and combine all host specific outputs of the [log4j-detector](https://github.com/mergebase/log4j-detector) logs in json format to one single CSV file.\n\n## Getting started  \n\n### With Python and pip installed\n\nInstall log4j-detector-to-csv with pip:\n```bash\npip install log4j-detector-to-csv\n```\n\nRun log4j-detector-to-csv:\n```bash\nlog4j-detector-to-csv -h\n```\n\nOutput:\n```bash\nusage: log4j-detector-to-csv [-h] -i INPUT -o OUTPUT\n\nConvert log4j-detector json file into one csv\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i INPUT, --input INPUT\n                        Input directory\n  -o OUTPUT, --output OUTPUT\n                        Output directory\n\n```\n\n### From Sourcecode\nPrerequisites:\n* python\n* poetry\n\nClone Repository:\n```bash\ngit clone https://github.com/richardbischof/log4j-detector-to-csv.git\n```\n\nChange in directory:\n```bash\ncd log4j-detector-to-csv/log4j_detector_to_csv\n```\n\nRun Script:\n```bash\npython main.py -i $INPUT_DIRECTORY -o $OUTPUT_FILE\n```\n\nExample:\n```bash \npython main.py -i logs -o report.csv\n```\n',
    'author': 'Richard Bischof',
    'author_email': 'richard.bischof@lgln.niedersachsen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/richardbischof/log4j-detector-to-csv',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
