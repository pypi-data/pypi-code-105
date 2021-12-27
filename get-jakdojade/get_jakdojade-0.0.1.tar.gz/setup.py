#!/usr/bin/env python

from os import path

from setuptools import find_packages
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

test_requirements = []
with open(path.join(this_directory, 'test_requirements.txt')) as f:
    for line in f:
        require = line.split('#', 1)[0].strip()
        if require:
            test_requirements.append(require)
setup(
    name='get_jakdojade',
    packages=find_packages(exclude=['tests']),
    version='0.0.1',
    url='https://github.com/Behoston/get_jakdojade',
    license='MIT',
    author='Behoston',
    author_email='mlegiecki@gmail.com',
    description='Jakdojade URL generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['get_jakdojade'],
    include_package_data=True,
    package_data={'get_jakdojade': ["py.typed"]},
    platforms='any',
    python_requires='>=3.6',
    tests_require=test_requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development',
        'Typing :: Typed',
    ],
)
