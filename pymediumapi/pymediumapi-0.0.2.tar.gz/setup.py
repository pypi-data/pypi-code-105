import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymediumapi",
    version="0.0.2",
    author="Andrea Grillo",
    author_email="andrea.grillo96@live.com",
    description="A python package to interact with Medium API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andregri/pymediumapi",
    project_urls={
        "Bug Tracker": "https://github.com/andregri/pymediumapi/issues",
    },
    install_requires = [
        "requests==2.26.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)