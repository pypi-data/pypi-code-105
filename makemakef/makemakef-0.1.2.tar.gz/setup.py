from setuptools import setup, find_packages


long_description = open('README.md', 'r', encoding='utf-8').read()

setup(
    name="makemakef",
    version="0.1.2",
    entry_points={
        'console_scripts': [
            'makemakef = makemakef.main:main',
        ]
    },
    author="Nkzono",
    author_email="71783375+Nkzono99@users.noreply.github.com",
    description="Command to create a Makefile to build nicely written Fortran code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nkzono99/camptools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
