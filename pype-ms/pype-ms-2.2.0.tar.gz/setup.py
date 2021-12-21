from setuptools import setup, find_packages
from version import VERSION


setup(
    author="Mathias Schreiner",
    author_email="matschreiner@gmail.com",
    url="https://gitlab.com/matschreiner/pype",
    download_url="https://gitlab.com/matschreiner/pype/-/archive/{VERSION}/pype-{VERSION}.tar.gz",
    name="pype-ms",
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "pytest",
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "pype = pype.cli:cli",
        ],
    },
)
