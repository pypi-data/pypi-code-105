import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xpt",
    version="0.0.1",
    author="AngWang",
    author_email="wangang.wa@alibaba-inc.com",
    description="Pytorch with XLA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alibaba",
    license='Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
