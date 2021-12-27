import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fgfw",
    version="0.0.3",  # Latest version .
    author="slipper",
    author_email="r2fscg@gmail.com",
    description="Fuck GFW",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private_repo/codefast",
    packages=setuptools.find_packages(),
    package_data={'fgfw': ['bin/*']},
    install_requires=['requests', 'codefast'],
    entry_points={'console_scripts': ['flibexec=fgfw.core:entry']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
