from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['jinja_subrender']

setup(
    name="jinja_subrender",

    version="0.0.1",
    # 0.0.1 - init release, render()

    packages=packages,
    install_requires=[
        'flask',
    ],

    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A simple way to render a Jinja2 template within another Jinja2 template.",
    long_description=long_description,
    license="PSF",
    keywords="grant miller flask jinja template render within subrender",
    url="https://github.com/GrantGMiller/jinja_subrender",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/jinja_subrender",
    }

)
