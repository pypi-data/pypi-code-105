import pathlib
from setuptools import setup

HERE=pathlib.Path(__file__).parent

setup(
    name ="flame-autob",
    version = "1.0.0",
    author = "Urmila",
    author_email = "urmilaraj18@gmail.com",
    description = "Anomaly detection on scientific datasets",
    long_description ="long_description",
    long_description_content_type = "text/markdown",
    license="MIT",
    classifiers = [
       "License :: OSI Approved :: MIT License",
       "Programming Language :: Python :: 3.6",
       "Programming Language :: Python :: 3.7",
       "Programming Language :: Python :: 3.8",
    ],
    packages=["flame_auto"],
    install_requires=["torch","numpy","matplotlib"],
)


