import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logtop",
    version="0.0.1",
    author="Valentyn Romaniuk",
    author_email="valik8355@gmail.com",
    description="Package for easy loging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RmValn/logtop",
    project_urls={
        "Bug Tracker": "https://github.com/RmValn/logtop/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
          'loguru',
      ],
    python_requires=">=3.6",
)