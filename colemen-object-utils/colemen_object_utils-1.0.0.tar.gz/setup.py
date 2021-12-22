# pylint: disable=line-too-long
'''
    Setup stuff.
'''
from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'Colemen Object Utils'
LONG_DESCRIPTION = 'Colemen Object Utils'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="colemen_object_utils",
    version=VERSION,
    author="Colemen Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=['colemen_object_utils', 'utils.dict'],
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=['colemen_string_utils'],

    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
