import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='termplayer',
    version="0.0.1",
    author="NeoClear",
    author_email="neoclear@outlook.com",
    description="A python program to help you play youtube playlists on your terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_required=[
      'git+https://github.com/Cupcakus/pafy',
      'youtube-dl==2021.12.17',
      'python-vlc==3.0.12118'
    ]
)
