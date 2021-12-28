import pathlib

import pkg_resources
import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setuptools.setup(
    name='Deep Learning Plus',
    version='0.0.1',
    author='Greenfrogs',
    author_email='5961364+greenfrogs@users.noreply.github.com',
    description='A collection of Python packages designed for the Python 3.9 for when you only want 1 import',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/greenfrogs/DeepLearningPlus',
    license='Apache License 2.0',
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    python_requires='==3.9',
)