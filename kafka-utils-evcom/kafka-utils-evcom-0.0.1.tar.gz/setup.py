import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kafka-utils-evcom",
    version="0.0.1",
    author="Matheus",
    author_email="matheus.fachinis@gmail.com",
    description="Some utils class to use confluent-kafka",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Evcom-Lab/kafka-utils",
    project_urls={
        "Bug Tracker": "https://github.com/Evcom-Lab/kafka-utils/issues",
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
