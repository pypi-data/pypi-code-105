import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webnew",
    version="1.1.1",
    author="BT.Q",
    author_email="2264481688@qq.com",
    description="A light library to build tiny websites 一个用于搭建轻量级网站的库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MinesomeBTQ/WebNew",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'web.py',
    ],
)