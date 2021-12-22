#!/usr/bin/env python3
import setuptools

# Workaround issue in pip with "pip install -e --user ."
import site
site.ENABLE_USER_SITE = True

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smartchem_ion3",
    version="1.0.0",
    author="Patrick Tapping",
    author_email="mail@patricktapping.com",
    description="Python interface to the SMARTChem-Ion3 ion-selective electrode instrument.",
    long_description=long_description,
    url="https://gitlab.com/ptapping/smartchem-ion3",
    project_urls={
        "Documentation": "https://smartchem-ion3.readthedocs.io/",
        "Source": "https://gitlab.com/ptapping/smartchem-ion3",
        "Tracker": "https://gitlab.com/ptapping/smartchem-ion3/-/issues",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pyserial"
    ],
)
