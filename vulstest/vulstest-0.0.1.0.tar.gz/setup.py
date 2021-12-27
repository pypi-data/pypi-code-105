# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
"""Setup for the clrprint package."""

#from distutils.core import setup
from setuptools import setup, Extension

setup(
    author="crazy",
    name='vulstest',
    version='v0.0.1.0',
    download_url='https://github.com/crazyfortests/vulstest/archive/refs/tags/v0.0.2.tar.gz',
    python_requires=">=3.2",
    packages=['vulstest'],
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
