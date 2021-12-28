import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytorchx",
    version="0.0.1",
    author="AngWang",
    author_email="wangang.wa@alibaba-inc.com",
    description="a small python pacakge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
