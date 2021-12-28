"""
Setup to create the package
"""
import polidoro_install
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='polidoro-install',
    version=polidoro_install.VERSION,
    description='Polidoro Install.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/heitorpolidoro/polidoro-install',
    author='Heitor Polidoro',
    scripts=['bin/polinstall'],
    license='unlicense',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    install_requires=['pyyaml', 'pydantic', 'requests'],
    include_package_data=True
)
