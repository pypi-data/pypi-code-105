import setuptools
from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="BnpInstaller",
    version="1.0.0",
    author="ArchLeaders",
    author_email="archleadership28@gmail.com",
    description="A simple CLI app to install bnp mods.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArchLeaders/BnpInstaller",
    include_package_data=True,
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts":
            ['BnpInstaller = BnpInstaller.BnpInstaller:main']
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.7",
    install_requires=['bcml>=3.0.0'],
)