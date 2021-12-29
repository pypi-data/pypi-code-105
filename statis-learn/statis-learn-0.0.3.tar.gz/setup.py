import setuptools

__version__ = '0.0.3'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="statis-learn",
    python_requires=">=3.5",
    version=__version__,
    author="Jim Chen",
    author_email="axfbh119@gmail.com",
    description="Statistics in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/axfbh/statis-learn",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    platforms=['linux', 'windows', 'macos'],
    install_requires=['numpy', 'scipy', 'pandas'],
)
