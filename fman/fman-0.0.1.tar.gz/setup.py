import setuptools

with open('README.md', 'r') as README:
    long_description = README.read()

with open('requirements.txt', 'r') as requirements:
    requirement = requirements.read().split('\n')

classifiers = [
    'Development Status :: 3 - Alpha',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setuptools.setup(
    name="fman",
    version="0.0.1",
    description="FMan - A external module for builtin works tool for Python 3 (open source).",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/almas-ali/fman",
    author="Md. Almas Ali",
    author_email="almaspr3@gmail.com",
    keyword="FMan, FileManager, Dataset, ClassExplore, DatasetClassExplore",
    license="MIT",
    classifiers=classifiers,
    packages=setuptools.find_packages(),
    install_requires=requirement,
)
