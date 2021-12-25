import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="str2int",
    version="1.0.4",
    author="Anish Gorakavi",
    author_email="anish.gorakavi@gmail.com",
    description="A simple module to suck intagers out of strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anishgorakavi787809/str2int",
    packages=setuptools.find_packages(),
    py_modules=['str2int'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)