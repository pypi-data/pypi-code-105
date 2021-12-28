#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Rutger Berns",
    author_email='rutgerb0000@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Removes shadows from jupyter notebook to create a flat styled experience.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='flat_styled_jupyter_notebooks',
    name='flat_styled_jupyter_notebooks',
    packages=find_packages(include=['flat_styled_jupyter_notebooks', 'flat_styled_jupyter_notebooks.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Rutger0000/flat_styled_jupyter_notebooks',
    version='0.1.0',
    zip_safe=False,
)
