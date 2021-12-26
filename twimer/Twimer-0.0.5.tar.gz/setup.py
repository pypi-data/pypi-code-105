import setuptools

with open("README.md", "r") as file:
    long_description = file.read()


setuptools.setup(
    name="Twimer",  # Replace with your own username
    version="0.0.5",
    author="Moein Kareshk",
    author_email="mkareshk@outlook.com",
    description="Stream Tweets into Your Favorite Databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkareshk/twimer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pymongo==4.0.1", "tweepy==3.9.0"],
    extras_require={"testing": ["pytest", "pytest-runner"]},
    python_requires=">=3.8",
)
