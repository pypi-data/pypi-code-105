import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TwsIBapi-projectX-IB",
    version="10.11.1.1",
    author="IBG LLC",
    author_email="nikolay.gyuneliev@gmail.com",
    description="A package downloaded directly from the official IB site",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ProjectIbX/TwsIBapi",
    project_urls={
        "Bug Tracker": "https://github.com/ProjectIbX/TwsIBapi/src",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)