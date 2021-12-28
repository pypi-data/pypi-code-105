# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
"""Setup for the clrprint package."""

#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    author="ajasdevtest",
    name='popmodule',
    version='v1.1',
    python_requires=">=3.2",
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Build Tools',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
)