import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chenyang",
    version="1.0.1",
    author="haha",
    author_email="haha@qq.com",
    license='MIT',
    description="Happy Everyday",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wjx2zuoshi/chenyang",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)