# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cutplace']

package_data = \
{'': ['*']}

install_requires = \
['XlsxWriter>=3,<4', 'xlrd>=1.2,<2.0']

entry_points = \
{'console_scripts': ['cutplace = cutplace.applications:main_for_script']}

setup_kwargs = {
    'name': 'cutplace',
    'version': '0.9.0',
    'description': 'validate data stored in CSV, PRN, ODS or Excel files',
    'long_description': ".. image:: https://img.shields.io/pypi/v/cutplace\n    :target: https://pypi.org/project/cutplace/\n    :alt: PyPI\n\n.. image:: https://readthedocs.org/projects/cutplace/badge/?version=latest\n    :target: https://cutplace.readthedocs.io/\n    :alt: Documentation\n\n.. image:: https://github.com/roskakori/cutplace/actions/workflows/build.yaml/badge.svg\n    :target: https://travis-ci.org/roskakori/cutplace\n    :alt: Build Status\n\n.. image:: https://coveralls.io/repos/roskakori/cutplace/badge.png?branch=master\n    :target: https://coveralls.io/r/roskakori/cutplace?branch=master\n    :alt: Test coverage\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Black\n\nCutplace is a tool and API to validate that tabular data stored in CSV,\nExcel, ODS and PRN files conform to a cutplace interface definition (CID).\n\nAs an example, consider the following ``customers.csv`` file that stores data\nabout customers::\n\n    customer_id,surname,first_name,born,gender\n    1,Beck,Tyler,1995-11-15,male\n    2,Gibson,Martin,1969-08-18,male\n    3,Hopkins,Chester,1982-12-19,male\n    4,Lopez,Tyler,1930-10-13,male\n    5,James,Ana,1943-08-10,female\n    6,Martin,Jon,1932-09-27,male\n    7,Knight,Carolyn,1977-05-25,female\n    8,Rose,Tammy,2004-01-12,female\n    9,Gutierrez,Reginald,2010-05-18,male\n    10,Phillips,Pauline,1960-11-09,female\n\nA CID can describe such a file in an easy to read way. It consists of\nthree sections. First, there is the general data format:\n\n==  ==============  ===========\n..  Property        Value\n==  ==============  ===========\nD   Format          Delimited\nD   Encoding        UTF-8\nD   Header          1\nD   Line delimiter  LF\nD   Item delimiter  ,\n==  ==============  ===========\n\nNext there are the fields stored in the data file:\n\n==  =============  ==========  =====  ======  ========  ==============================\n..  Name           Example     Empty  Length  Type      Rule\n==  =============  ==========  =====  ======  ========  ==============================\nF   customer_id    3798                       Integer   0...99999\nF   surname        Miller             ...60\nF   first_name     John        X      ...60\nF   date_of_birth  1978-11-27                 DateTime  YYYY-MM-DD\nF   gender         male        X              Choice    female, male\n==  =============  ==========  =====  ======  ========  ==============================\n\nOptionally you can describe conditions that must be met across the whole file:\n\n==  =======================  ========  ===========\n..  Description              Type      Rule\n==  =======================  ========  ===========\nC   customer must be unique  IsUnique  customer_id\n==  =======================  ========  ===========\n\nThe CID can be stored in common spreadsheet formats, in particular\nExcel and ODS, for example ``cid_customers.ods``.\n\nCutplace can validate that the data file conforms to the CID::\n\n    $ cutplace cid_customers.ods customers.csv\n\nNow add a new line with a broken ``date_of_birth``::\n\n    73921,Harris,Diana,04.08.1953,female\n\nCutplace rejects this file with the error message:\n\n    customers.csv (R12C4): cannot accept field 'date_of_birth': date must\n    match format YYYY-MM-DD (%Y-%m-%d) but is: '04.08.1953'\n\nAdditionally, cutplace provides an easy to use API to read and write\ntabular data files using a common interface without having to deal with\nthe intrinsic of data format specific modules. To read and validate the\nabove example::\n\n    import cutplace\n    import cutplace.errors\n\n    cid_path = 'cid_customers.ods'\n    data_path = 'customers.csv'\n    try:\n        for row in cutplace.rows(cid_path, data_path):\n            pass  # We could also do something useful with the data in ``row`` here.\n    except cutplace.errors.DataError as error:\n        print(error)\n\nFor more information, read the documentation at\nhttp://cutplace.readthedocs.org/ or visit the project at\nhttps://github.com/roskakori/cutplace.\n",
    'author': 'Thomas Aglassinger',
    'author_email': 'roskakori@users.sourceforge.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roskakori/cutplace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
