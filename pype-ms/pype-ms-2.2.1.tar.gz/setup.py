from setuptools import setup, find_packages


version_path = 'version.py'
with open(version_path) as ver_file:
    exec(ver_file.read()) # pylint: disable=exec-used


setup(
    author="Mathias Schreiner",
    author_email="matschreiner@gmail.com",
    url="https://gitlab.com/matschreiner/pype",
    download_url="https://gitlab.com/matschreiner/pype/-/archive/{__version__}/pype-{__version__}.tar.gz",
    name="pype-ms",
    version=__version__,
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
