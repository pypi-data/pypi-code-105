# Copyright (c) 2021 Trelent Inc.

# External modules
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trelent",
    author="Trelent Inc.",
    author_email="contact@trelent.net",
    description="A command line tool to generate documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://trelent.net",
    version='1.0',
    py_modules=['trelent.auth_module', 'trelent.docgen', 'trelent.main', 'trelent.utils'],
    install_requires=[
        'Click',
        'Requests'
    ],
    entry_points='''
        [console_scripts]
        trelent=trelent.main:trelent
    ''',
    classifiers=[
        "Operating System :: OS Independent",
    ],
)