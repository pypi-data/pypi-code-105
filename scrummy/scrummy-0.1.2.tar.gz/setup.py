import pathlib
from setuptools import setup, find_packages

from scrummy import __version__

HERE: pathlib.Path = pathlib.Path(__file__).parent
README: str = (HERE / "README.md").read_text()

setup(
    name='scrummy',
    version=__version__.__version__,
    description=__version__.__description__,
    long_description=README,
    long_description_content_type="text/markdown",
    author=__version__.__author__,
    author_email=__version__.__author_email__,
    license=__version__.__license__,
    url=__version__.__url__,
    project_urls={
        'Homepage': __version__.__url__,
        'Source': __version__.__url__,
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click', 'python-dateutil', 'xdg'],
    entry_points={
        'console_scripts': [
            'scrummy = scrummy.main:cli',
        ]
    }
)
