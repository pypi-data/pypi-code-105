import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytyping",
    version="0.0.1",
    author="Francesco Cappetti",
    author_email="f.cappetti.05@gmail.com",
    description="A simple typing speed test right in your terminal made with Python and the curses module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/francescocappetti/pytyping",
    project_urls={
        "Bug Tracker": "https://github.com/francescocappetti/pytyping/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': ['pytyping=pytyping.app:run'],
    },
)
