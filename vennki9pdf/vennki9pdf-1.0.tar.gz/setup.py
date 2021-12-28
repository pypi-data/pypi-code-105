import setuptools
from pathlib import Path

# Call setup method and pass keyword arguments
setuptools.setup(
    name='vennki9pdf',  # specify a unique name for our package as it shouldn't conflict with other packages in Pypi repository
    version='1.0',  # specify a version number for our package
    # content of the README.md file
    long_description=Path('README.md').read_text(),
    # What packages are going to be distributed, we need to tell setup tools about the modules and the packages
    # that we are going to publish
    # This method will look at our project and automatically discover the packages that we defined.
    packages=setuptools.find_packages(exclude=['tests', 'data'])
    # We need to tell it to exclude two directories
)
