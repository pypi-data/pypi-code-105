from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'A basic package for helping Sloths team to find a current scraping type for a site'
LONG_DESCRIPTION = 'A basic package for helping Sloths team to find a current scraping type for a site'

# Setting up
setup(
    name="scrapingtype",
    version=VERSION,
    author="VladimirSavchenko",
    author_email="savchenko.vldmr@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['python-consul'],
    keywords=['Sloths', '360', 'scraping'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)