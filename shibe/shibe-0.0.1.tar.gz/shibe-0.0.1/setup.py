import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shibe",
    version="0.0.1",
    author="GoldenCorgi",
    description="Placeholder for future work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoldenCorgi/shibe",
    project_urls={
        "Bug Tracker": "https://github.com/GoldenCorgi/shibe/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "IU"},
    packages=setuptools.find_packages(where=""),
    python_requires=">=3.6",
)
