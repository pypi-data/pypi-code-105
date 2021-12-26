# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
"""Setup for the clrprint package."""

#from distutils.core import setup
from setuptools import setup, Extension

setup(
    author="ajdev",
    name='tstvuln',
    version='v1.1',
    python_requires=">=3.2",
    packages=['tstvuln'],
    download_url='https://github.com/crazyfortests/tstvuln/archive/refs/tags/v1.1.tar.gz',
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
